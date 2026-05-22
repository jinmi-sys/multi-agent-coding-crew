"""Tests for sandbox."""

import os
from multi_agent_coding_crew.sandbox.runner import Sandbox


class TestSandbox:
    def test_context_manager(self):
        with Sandbox() as sb:
            assert os.path.exists(sb.path)
            result = sb.run("echo sandbox")
            assert result.success
            assert "sandbox" in result.stdout
        assert not os.path.exists(sb.path)

    def test_write_file(self):
        with Sandbox() as sb:
            path = sb.write_file("test.py", "print(42)")
            assert os.path.exists(path)
            result = sb.run("python test.py")
            assert result.success
            assert "42" in result.stdout

    def test_sandbox_isolation(self):
        paths = []
        with Sandbox() as sb1:
            paths.append(sb1.path)
        with Sandbox() as sb2:
            paths.append(sb2.path)
        assert paths[0] != paths[1]
