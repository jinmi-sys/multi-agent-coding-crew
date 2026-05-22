"""Tests for agent definitions."""

from multi_agent_coding_crew.agents.definitions import (
    AgentRole, AgentProfile, AGENT_REGISTRY,
    ARCHITECT, DEVELOPER, REVIEWER, TESTER, OPS,
)


class TestAgentDefinitions:
    def test_registry_has_five_agents(self):
        assert len(AGENT_REGISTRY) == 5

    def test_all_roles_in_registry(self):
        for role in AgentRole:
            assert role in AGENT_REGISTRY

    def test_architect_profile(self):
        assert ARCHITECT.role == AgentRole.ARCHITECT
        assert ARCHITECT.name == "Architect"
        assert "architect" in ARCHITECT.system_prompt.lower()
        assert ARCHITECT.temperature == 0.2

    def test_developer_profile(self):
        assert DEVELOPER.role == AgentRole.DEVELOPER
        assert DEVELOPER.max_iterations == 10
        assert "file_write" in DEVELOPER.tools

    def test_reviewer_temperature(self):
        assert REVIEWER.temperature == 0.1  # most conservative

    def test_tester_has_shell(self):
        assert "shell_exec" in TESTER.tools

    def test_ops_profile(self):
        assert OPS.role == AgentRole.OPS
        assert "deployment" in OPS.system_prompt.lower()
