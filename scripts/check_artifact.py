from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

MODEL_SUFFIXES = {".bin", ".pt", ".pth", ".npz", ".safetensors", ".lzma", ".zst", ".zstd", ".gz"}


def iter_record_dirs(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_dir() and (path / "submission.json").exists():
            yield path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-root", default="records")
    parser.add_argument("--budget-bytes", type=int, default=16_000_000)
    parser.add_argument("--allow-missing-model", action="store_true")
    args = parser.parse_args()

    candidate_root = Path(args.candidate_root).resolve()
    if not candidate_root.exists():
        print(f"{candidate_root} does not exist; nothing to check.")
        return 0

    errors: list[str] = []
    checked = 0

    for record_dir in iter_record_dirs(candidate_root):
        checked += 1
        train_script = record_dir / "train_gpt.py"
        code_bytes = train_script.stat().st_size if train_script.exists() else 0

        model_files = [
            p for p in record_dir.iterdir()
            if p.is_file() and p.suffix.lower() in MODEL_SUFFIXES and p.name != "train_gpt.py"
        ]

        if not model_files:
            if args.allow_missing_model:
                print(f"{record_dir}: no model artifact found yet; skipping size total.")
                continue
            errors.append(f"{record_dir}: no model artifact found")
            continue

        largest_model = max(model_files, key=lambda p: p.stat().st_size)
        model_bytes = largest_model.stat().st_size
        total = code_bytes + model_bytes

        print(
            f"{record_dir}: code={code_bytes} model={model_bytes} total={total} "
            f"budget={args.budget_bytes}"
        )

        if total > args.budget_bytes:
            errors.append(
                f"{record_dir}: artifact budget exceeded "
                f"({total} > {args.budget_bytes}) using model {largest_model.name}"
            )

    if checked == 0:
        print("No candidate record directories found.")
        return 0

    if errors:
        print("Artifact check failed:")
        for err in errors:
            print(f" - {err}")
        return 1

    print("Artifact check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
