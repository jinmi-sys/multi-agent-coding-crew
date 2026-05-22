"""Tests for file and shell tools."""

import pytest
import tempfile
import os

from multi_agent_coding_crew.tools.file_ops import FileOps
from multi_agent_coding_crew.tools.shell_ops import ShellOps


class TestFileOps:
    def test_write_and_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            ops = FileOps(tmp)
            ops.write("test.txt", "hello world")
            assert ops.read("test.txt") == "hello world"

    def test_list_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            ops = FileOps(tmp)
            ops.write("a.txt", "a")
            ops.write("b.txt", "b")
            items = ops.list_dir(".")
            assert "a.txt" in items
            assert "b.txt" in items

    def test_path_escape_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            ops = FileOps(tmp)
            with pytest.raises(PermissionError):
                ops.read("../../etc/passwd")

    def test_read_missing_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            ops = FileOps(tmp)
            with pytest.raises(FileNotFoundError):
                ops.read("nope.txt")

    def test_delete_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            ops = FileOps(tmp)
            ops.write("del.txt", "bye")
            result = ops.delete("del.txt")
            assert "Deleted" in result


class TestShellOps:
    def test_execute_echo(self):
        with tempfile.TemporaryDirectory() as tmp:
            shell = ShellOps(tmp, timeout=5)
            result = shell.execute("echo hello")
            assert result.success
            assert "hello" in result.stdout

    def test_blocked_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            shell = ShellOps(tmp)
            result = shell.execute("rm -rf /")
            assert not result.success
            assert "blocked" in result.stderr.lower()

    def test_timeout(self):
        with tempfile.TemporaryDirectory() as tmp:
            shell = ShellOps(tmp, timeout=1)
            result = shell.execute("sleep 10")
            assert not result.success
