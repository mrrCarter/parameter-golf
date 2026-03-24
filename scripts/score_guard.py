from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--history", default="results/history.csv")
    parser.add_argument("--candidate-json", default="results/latest_candidate.json")
    parser.add_argument("--allow-missing", action="store_true")
    parser.add_argument("--warn-delta", type=float, default=0.002)
    args = parser.parse_args()

    history_path = Path(args.history)
    candidate_path = Path(args.candidate_json)

    if not history_path.exists() or not candidate_path.exists():
        if args.allow_missing:
            print("Score guard skipped because history or candidate JSON is missing.")
            return 0
        print("Score guard failed: missing history or candidate JSON.")
        return 1

    with history_path.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    if not rows:
        if args.allow_missing:
            print("Score guard skipped because history is empty.")
            return 0
        print("Score guard failed: history.csv has no rows.")
        return 1

    try:
        best_prev = min(float(row["val_bpb"]) for row in rows)
    except Exception as exc:  # noqa: BLE001
        print(f"Score guard failed while reading history.csv: {exc}")
        return 1

    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    current = float(candidate["val_bpb"])

    delta = current - best_prev
    print(f"Previous best: {best_prev:.6f}")
    print(f"Candidate:     {current:.6f}")
    print(f"Delta:         {delta:+.6f}")

    if delta > args.warn_delta:
        print(
            "Warning: candidate is materially worse than previous best. "
            "This does not fail the build, but you should justify it."
        )
    else:
        print("Score guard passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
