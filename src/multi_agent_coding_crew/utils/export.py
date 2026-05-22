"""Export run results to various formats."""

import json
from pathlib import Path
from typing import Any


def export_json(data: dict[str, Any], path: str) -> str:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    return str(target)


def export_markdown(run_summary: dict[str, Any], path: str) -> str:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Coding Crew Run Report",
        "",
        f"**Task:** {run_summary.get('task', 'N/A')}",
        f"**Success:** {run_summary.get('success', False)}",
        f"**Duration:** {run_summary.get('duration_sec', 0)}s",
        f"**Total Tokens:** {run_summary.get('total_tokens', 0)}",
        f"**Phases:** {run_summary.get('phases', 0)}",
        "",
        "---",
        "",
    ]
    target.write_text("\n".join(lines), encoding="utf-8")
    return str(target)
