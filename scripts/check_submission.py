from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

REQUIRED_RECORD_FILES = {"README.md", "submission.json"}
TRAIN_SCRIPT_PREFIX = "train_gpt"
TRAIN_SCRIPT_SUFFIX = ".py"
LOG_SUFFIXES = {".log", ".txt", ".tsv"}


def iter_record_dirs(records_root: Path) -> Iterable[Path]:
    if not records_root.exists():
        return []
    for path in records_root.rglob("*"):
        if path.is_dir() and (path / "submission.json").exists():
            yield path


def validate_submission_json(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"{path}: invalid JSON ({exc})"], []

    name_keys = {"name", "run_name"}
    author_keys = {"github_id", "author"}
    bpb_keys = {"val_bpb", "mean_val_bpb"}
    fallback_metric_keys = {"val_loss", "mean_val_loss"}

    if not any(key in data for key in name_keys):
        warnings.append(
            f"{path}: missing run name key (expected one of {sorted(name_keys)})"
        )
    if not any(key in data for key in author_keys):
        warnings.append(
            f"{path}: missing author key (expected one of {sorted(author_keys)})"
        )

    bpb_present = [key for key in bpb_keys if key in data]
    metric_present = bpb_present or [key for key in fallback_metric_keys if key in data]
    if not metric_present:
        warnings.append(
            f"{path}: missing metric key (expected one of "
            f"{sorted(bpb_keys | fallback_metric_keys)})"
        )
    for key in metric_present:
        if not isinstance(data.get(key), (int, float)):
            errors.append(f"{path}: `{key}` must be numeric")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Repository root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    records_root = root / "records"

    if not records_root.exists():
        print("records/ directory not found; nothing to validate.")
        return 0

    errors: list[str] = []
    warnings: list[str] = []
    found_any = False

    for record_dir in iter_record_dirs(records_root):
        found_any = True
        names = {p.name for p in record_dir.iterdir() if p.is_file()}

        missing = sorted(REQUIRED_RECORD_FILES - names)
        if missing:
            errors.append(f"{record_dir}: missing required files {missing}")

        has_train_script = any(
            p.is_file()
            and p.suffix == TRAIN_SCRIPT_SUFFIX
            and p.name.startswith(TRAIN_SCRIPT_PREFIX)
            for p in record_dir.iterdir()
        )
        if not has_train_script:
            errors.append(
                f"{record_dir}: missing train script "
                f"(expected `{TRAIN_SCRIPT_PREFIX}*{TRAIN_SCRIPT_SUFFIX}`)"
            )

        has_log = any(p.suffix in LOG_SUFFIXES for p in record_dir.iterdir() if p.is_file())
        if not has_log:
            errors.append(
                f"{record_dir}: missing evidence file "
                "(expected one of .log, .txt, .tsv)"
            )

        submission_path = record_dir / "submission.json"
        if submission_path.exists():
            submit_errors, submit_warnings = validate_submission_json(submission_path)
            errors.extend(submit_errors)
            warnings.extend(submit_warnings)

    if not found_any:
        print("No candidate record directories found under records/.")
        return 0

    if errors:
        print("Submission validation failed:")
        for err in errors:
            print(f" - {err}")
        return 1

    if warnings:
        print("Submission validation warnings:")
        for warning in warnings:
            print(f" - {warning}")

    print("Submission validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
