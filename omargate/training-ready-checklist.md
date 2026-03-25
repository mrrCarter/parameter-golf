# Parameter Golf Training-Ready Checklist

This runbook connects local validation, Omar Gate policy review, and evidence tracking for this fork.

## What is wired

- PR static gate: `.github/workflows/pr-inner-loop.yml`
- PR Omar Gate: `.github/workflows/pr-inner-loop.yml`
- Omar comment/manual command: `.github/workflows/omar-gate-on-command.yml`
- Manual deep audit: `.github/workflows/nightly-deep-audit.yml`
- Local Omar action install path: `.github/actions/sentinelayer-v1-action/`
- Challenge spec for auto-discovery binding: `omargate/parameter-golf-spec.md`
- Challenge legality scripts: `scripts/`

Omar Gate workflows run with:

- `spec_binding_mode: auto_discovered`
- `model_training_intent: parameter-golf`

PR gate runs automatically on every PR.

Comment commands accepted on PRs (from OWNER/MEMBER/COLLABORATOR), plus `workflow_dispatch` manual runs:

- `/omar` (defaults to `deep` + `P1`)
- `/omar baseline`
- `/omar audit p0`

## Credentials and prerequisites

- `SENTINELAYER_TOKEN` must exist in GitHub Actions secrets for this repo.
- Python 3.11+ is required for local static checks.
- Real model training/eval still runs on your GPU environment (Runpod/self-hosted), not on GitHub-hosted runners.

## Local pre-PR gate

From repo root:

```bash
python -m compileall records scripts .github/actions/sentinelayer-v1-action/src
python scripts/check_submission.py --root .
python scripts/check_no_forbidden_calls.py --path records
python scripts/check_artifact.py --candidate-root records --budget-bytes 16000000 --allow-missing-model
python scripts/check_assignment_limits.py --candidate-root records --allow-missing
python scripts/score_guard.py --history results/history.csv --candidate-json results/latest_candidate.json --allow-missing
```

## Training commands (smoke + real)

Local smoke (small run for code path confidence):

```bash
RUN_ID=smoke_local \
ITERATIONS=200 \
TRAIN_BATCH_TOKENS=8192 \
VAL_LOSS_EVERY=0 \
VAL_BATCH_SIZE=8192 \
python train_gpt_mlx.py
```

GPU candidate run template:

```bash
RUN_ID=<your_run_name> \
DATA_PATH=./data/datasets/fineweb10B_sp1024/ \
TOKENIZER_PATH=./data/tokenizers/fineweb_1024_bpe.model \
VOCAB_SIZE=1024 \
torchrun --standalone --nproc_per_node=1 train_gpt.py
```

8xH100 scale check template:

```bash
RUN_ID=<your_run_name> \
DATA_PATH=./data/datasets/fineweb10B_sp1024/ \
TOKENIZER_PATH=./data/tokenizers/fineweb_1024_bpe.model \
VOCAB_SIZE=1024 \
torchrun --standalone --nproc_per_node=8 train_gpt.py
```

## Training/eval evidence discipline

For each candidate under `records/track_10min_16mb/<run_name>/`:

1. Keep `train_gpt.py`, `README.md`, `submission.json`, and logs together.
2. Report measured `train_seconds`, `eval_seconds`, and `artifact_total_bytes` in `submission.json` when available.
3. Update `results/latest_candidate.json` and append to `results/history.csv` after real runs.
4. Keep README claims tied to specific logs/seeds.
5. Update candidate README with: what changed, why, expected improvement, and what still needs testing.

## Progress log (2026-03-24)

- What changed: connected `parameter-golf` workflows to local `sentinelayer-v1-action`, enabled model-training context, added static challenge validation, and switched Omar execution to PR comment commands only.
- What changed: connected `parameter-golf` workflows to local `sentinelayer-v1-action`, enabled model-training context, added static challenge validation, restored automatic PR Omar Gate, and retained on-command Omar runs.
- Why: remove external version drift, enforce challenge legality continuously, and align Omar context with model-training repos.
- What we expect to improve: fewer broken PRs, clearer policy routing, and better reproducibility/evidence hygiene before expensive GPU runs.
- What still needs testing: first PR comment command run (`/omar audit p0`) plus one full candidate evidence cycle (`results/latest_candidate.json` + `results/history.csv` updated from a real training run).
