"""Shell execution tools for agents."""

import subprocess
import shlex
from dataclasses import dataclass
from typing import Optional


BLOCKED_COMMANDS = {
    "rm -rf /", "mkfs", "dd if=", ":(){ :|:& };:",
    "chmod -R 777 /", "wget", "curl|sh",
}


@dataclass
class ShellResult:
    command: str
    stdout: str
    stderr: str
    returncode: int
    success: bool


class ShellOps:
    """Sandboxed shell command execution."""

    def __init__(self, workspace: str, timeout: int = 30):
        self.workspace = workspace
        self.timeout = timeout

    def _is_blocked(self, command: str) -> bool:
        cmd_lower = command.lower().strip()
        return any(blocked in cmd_lower for blocked in BLOCKED_COMMANDS)

    def execute(self, command: str) -> ShellResult:
        if self._is_blocked(command):
            return ShellResult(
                command=command, stdout="", stderr="Command blocked by safety filter",
                returncode=1, success=False,
            )
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True,
                timeout=self.timeout, cwd=self.workspace,
            )
            return ShellResult(
                command=command, stdout=result.stdout, stderr=result.stderr,
                returncode=result.returncode, success=result.returncode == 0,
            )
        except subprocess.TimeoutExpired:
            return ShellResult(
                command=command, stdout="", stderr=f"Timeout after {self.timeout}s",
                returncode=-1, success=False,
            )
        except Exception as e:
            return ShellResult(
                command=command, stdout="", stderr=str(e),
                returncode=-1, success=False,
            )
