from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

LIMIT_FIELDS = (
    ("train_seconds", 600.0),
    ("eval_seconds", 600.0),
    ("artifact_total_bytes", 16_000_000.0),
)


def iter_record_dirs(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_dir() and (path / "submission.json").exists():
            yield path


def _as_float(value: object) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-root", default="records")
    parser.add_argument("--max-train-seconds", type=float, default=600.0)
    parser.add_argument("--max-eval-seconds", type=float, default=600.0)
    parser.add_argument("--max-artifact-bytes", type=float, default=16_000_000.0)
    parser.add_argument(
        "--allow-missing",
        action="store_true",
        help="Allow missing optional limit fields and only validate fields that are present.",
    )
    args = parser.parse_args()

    candidate_root = Path(args.candidate_root).resolve()
    if not candidate_root.exists():
        print(f"{candidate_root} does not exist; nothing to check.")
        return 0

    effective_limits = {
        "train_seconds": float(args.max_train_seconds),
        "eval_seconds": float(args.max_eval_seconds),
        "artifact_total_bytes": float(args.max_artifact_bytes),
    }

    errors: list[str] = []
    checked = 0
    for record_dir in iter_record_dirs(candidate_root):
        checked += 1
        submission_path = record_dir / "submission.json"
        try:
            submission = json.loads(submission_path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{submission_path}: invalid JSON ({exc})")
            continue

        for field_name, default_limit in LIMIT_FIELDS:
            value = submission.get(field_name)
            limit = effective_limits.get(field_name, default_limit)
            if value is None:
                if args.allow_missing:
                    continue
                errors.append(f"{submission_path}: missing `{field_name}`")
                continue
            numeric = _as_float(value)
            if numeric is None:
                errors.append(f"{submission_path}: `{field_name}` must be numeric")
                continue
            if numeric > limit:
                errors.append(
                    f"{submission_path}: `{field_name}` exceeds limit "
                    f"({numeric} > {limit})"
                )

    if checked == 0:
        print("No candidate record directories found.")
        return 0

    if errors:
        print("Assignment-limit check failed:")
        for err in errors:
            print(f" - {err}")
        return 1

    print("Assignment-limit check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
