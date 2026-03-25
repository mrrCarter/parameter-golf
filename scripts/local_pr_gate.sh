#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[1/6] Compile Python"
python -m compileall records scripts .github/actions/sentinelayer-v1-action/src

echo "[2/6] Check submission structure"
python scripts/check_submission.py --root .

echo "[3/6] Check forbidden patterns"
python scripts/check_no_forbidden_calls.py --path records

echo "[4/6] Check artifact budget (if model files exist)"
python scripts/check_artifact.py --candidate-root records --budget-bytes 16000000 --allow-missing-model

echo "[5/6] Check assignment limits (if fields exist)"
python scripts/check_assignment_limits.py --candidate-root records --allow-missing

echo "[6/6] Optional score regression guard"
python scripts/score_guard.py --history results/history.csv --candidate-json results/latest_candidate.json --allow-missing

echo "All local PR gates passed."
