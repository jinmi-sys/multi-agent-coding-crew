"""Tests for utilities."""

import json
import tempfile
import os

from multi_agent_coding_crew.utils.token_counter import (
    estimate_tokens, fits_in_context, context_usage_pct,
)
from multi_agent_coding_crew.utils.export import export_json, export_markdown


class TestTokenCounter:
    def test_empty(self):
        assert estimate_tokens("") == 0

    def test_short_text(self):
        tokens = estimate_tokens("hello world")
        assert 2 <= tokens <= 4

    def test_fits_in_context(self):
        assert fits_in_context("short text", max_tokens=1000)
        assert not fits_in_context("x" * 100000, max_tokens=100)

    def test_usage_pct(self):
        pct = context_usage_pct("hello", max_tokens=100)
        assert 0 < pct < 100


class TestExport:
    def test_export_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "out.json")
            export_json({"key": "value"}, path)
            with open(path) as f:
                data = json.load(f)
            assert data["key"] == "value"

    def test_export_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "report.md")
            export_markdown({"task": "test", "success": True, "duration_sec": 1.5, "total_tokens": 100, "phases": 3}, path)
            content = open(path).read()
            assert "test" in content
            assert "Coding Crew" in content
