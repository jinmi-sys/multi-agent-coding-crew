"""Isolated sandbox for code execution."""

import os
import tempfile
import shutil
from pathlib import Path
from typing import Optional

from ..tools.shell_ops import ShellOps, ShellResult


class Sandbox:
    """Temporary isolated workspace for agent code execution."""

    def __init__(self, prefix: str = "coding-crew-"):
        self._tmpdir: Optional[str] = None
        self.prefix = prefix
        self.shell: Optional[ShellOps] = None

    def __enter__(self) -> "Sandbox":
        self._tmpdir = tempfile.mkdtemp(prefix=self.prefix)
        self.shell = ShellOps(self._tmpdir)
        return self

    def __exit__(self, *args) -> None:
        if self._tmpdir and os.path.exists(self._tmpdir):
            shutil.rmtree(self._tmpdir, ignore_errors=True)

    @property
    def path(self) -> str:
        return self._tmpdir or ""

    def run(self, command: str) -> ShellResult:
        if not self.shell:
            raise RuntimeError("Sandbox not initialized. Use 'with Sandbox() as sb:'")
        return self.shell.execute(command)

    def write_file(self, rel_path: str, content: str) -> str:
        if not self._tmpdir:
            raise RuntimeError("Sandbox not initialized")
        full = Path(self._tmpdir) / rel_path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content, encoding="utf-8")
        return str(full)
