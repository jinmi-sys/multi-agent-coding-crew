"""File operation tools for agents."""

import os
from pathlib import Path
from typing import Optional


class FileOps:
    """Safe file operations with sandboxed paths."""

    def __init__(self, workspace: str):
        self.workspace = Path(workspace).resolve()

    def _validate_path(self, path: str) -> Path:
        resolved = (self.workspace / path).resolve()
        if not str(resolved).startswith(str(self.workspace)):
            raise PermissionError(f"Path {path} escapes workspace")
        return resolved

    def read(self, path: str) -> str:
        target = self._validate_path(path)
        if not target.exists():
            raise FileNotFoundError(f"File not found: {path}")
        return target.read_text(encoding="utf-8")

    def write(self, path: str, content: str) -> str:
        target = self._validate_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"Written {len(content)} bytes to {path}"

    def list_dir(self, path: str = ".") -> list[str]:
        target = self._validate_path(path)
        if not target.is_dir():
            raise NotADirectoryError(f"Not a directory: {path}")
        return sorted(os.listdir(target))

    def delete(self, path: str) -> str:
        target = self._validate_path(path)
        if target.is_file():
            target.unlink()
            return f"Deleted file: {path}"
        raise ValueError(f"Cannot delete: {path} (not a regular file)")
