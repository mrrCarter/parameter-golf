from __future__ import annotations

import argparse
from pathlib import Path

FORBIDDEN_SNIPPETS = {
    "requests.": "Network calls should not be added to candidate code paths.",
    "httpx.": "Network calls should not be added to candidate code paths.",
    "urllib.request": "Network calls should not be added to candidate code paths.",
    "socket.": "Raw sockets are suspicious in challenge code.",
    "wget ": "External downloads are suspicious in challenge code.",
    "curl ": "External downloads are suspicious in challenge code.",
    "openai.": "Do not call remote APIs from candidate training/eval code.",
    "anthropic.": "Do not call remote APIs from candidate training/eval code.",
    "huggingface_hub": "Do not download artifacts at evaluation time.",
}

ALLOWED_EXTENSIONS = {".py", ".sh", ".md", ".txt", ".json", ".yml", ".yaml"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default="records")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"{root} does not exist; nothing to scan.")
        return 0

    findings: list[str] = []
    for file in root.rglob("*"):
        if not file.is_file():
            continue
        if file.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue
        text = file.read_text(encoding="utf-8", errors="ignore")
        for needle, reason in FORBIDDEN_SNIPPETS.items():
            if needle in text:
                findings.append(f"{file}: found '{needle}' -> {reason}")

    if findings:
        print("Forbidden-pattern scan failed:")
        for finding in findings:
            print(f" - {finding}")
        return 1

    print("Forbidden-pattern scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
