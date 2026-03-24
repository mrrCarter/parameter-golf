# Repository-wide instructions for AI coding agents

This repository is a lab for the OpenAI Parameter Golf challenge.

## Hard constraints

- Never add network calls to training or evaluation code.
- Never add code that reads extra datasets during evaluation.
- Never train on future validation tokens before they are scored.
- Keep leaderboard candidates self-contained.
- Keep counted submission code in the candidate `train_gpt.py`.
- Do not touch tokenizer or dataset code unless explicitly asked.
- Prefer one experimental change per PR.
- Never claim a score without a log or machine-readable evidence file.
- Do not mark a task complete until local validation passes.

## Files you may modify by default

- `records/**`
- `scripts/**`
- `.github/workflows/**`
- `AGENTS.md`
- `.github/instructions/**`

## Files to avoid unless explicitly asked

- shared infra outside this repo
- production secrets
- unrelated workflows
- broad refactors

## Required validation before finishing

Run:
- `bash scripts/local_pr_gate.sh`
- any experiment-specific command listed in the candidate README

## Preferred behavior

- explain changes clearly
- keep diffs small
- write comments only when they help
- preserve reproducibility
- write down assumptions in the candidate README
