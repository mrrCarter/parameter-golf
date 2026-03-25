from __future__ import annotations

import json
import os
from pathlib import Path


def _write_output(name: str, value: str) -> None:
    output_path = str(os.environ.get("GITHUB_OUTPUT") or "").strip()
    if not output_path:
        return
    with open(output_path, "a", encoding="utf-8") as handle:
        handle.write(f"{name}={value}\n")


def main() -> int:
    workspace = Path(str(os.environ.get("GITHUB_WORKSPACE") or ".")).resolve()
    spec_path = workspace / "omargate" / "parameter-golf-spec.md"
    if not spec_path.exists():
        raise RuntimeError(
            "Missing required Parameter Golf Omar spec at omargate/parameter-golf-spec.md"
        )

    context_dir = workspace / ".sentinelayer" / "context"
    context_dir.mkdir(parents=True, exist_ok=True)
    context_path = context_dir / "parameter-golf-review-context.json"

    context_payload = {
        "review_profile": "parameter-golf",
        "model_training_intent": "parameter-golf",
        "spec_binding_mode": "auto_discovered",
        "spec_path": "omargate/parameter-golf-spec.md",
        "scan_mode_default": str(os.environ.get("INPUT_SCAN_MODE") or "deep").strip() or "deep",
        "focus_areas": [
            "challenge legality",
            "validation leakage",
            "forbidden network/download paths",
            "artifact and runtime evidence",
            "workflow safety",
        ],
    }
    context_path.write_text(
        json.dumps(context_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    _write_output("model_training_intent", "parameter-golf")
    _write_output("spec_binding_mode", "auto_discovered")
    _write_output("context_artifact", str(context_path.relative_to(workspace)).replace("\\", "/"))
    print(
        "::notice::Parameter Golf Omar context prepared "
        f"(spec=omargate/parameter-golf-spec.md, context={context_path.name})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
