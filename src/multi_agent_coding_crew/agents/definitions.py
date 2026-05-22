"""Agent role definitions for the coding crew."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class AgentRole(Enum):
    ARCHITECT = "architect"
    DEVELOPER = "developer"
    REVIEWER = "reviewer"
    TESTER = "tester"
    OPS = "ops"


@dataclass
class AgentProfile:
    role: AgentRole
    name: str
    system_prompt: str
    tools: list[str] = field(default_factory=list)
    max_iterations: int = 5
    temperature: float = 0.3


ARCHITECT = AgentProfile(
    role=AgentRole.ARCHITECT,
    name="Architect",
    system_prompt=(
        "You are a senior software architect. Your job is to analyze requirements, "
        "design system architecture, select appropriate tech stacks, and define module "
        "boundaries. Output structured decisions with rationale. Consider scalability, "
        "maintainability, and security from the start."
    ),
    tools=["file_read", "web_search"],
    temperature=0.2,
)

DEVELOPER = AgentProfile(
    role=AgentRole.DEVELOPER,
    name="Developer",
    system_prompt=(
        "You are a senior full-stack developer. Write clean, well-documented code "
        "following the architecture decisions provided. Use type hints, proper error "
        "handling, and follow language idioms. Implement features incrementally and "
        "commit working code."
    ),
    tools=["file_read", "file_write", "shell_exec", "git_ops"],
    max_iterations=10,
    temperature=0.3,
)

REVIEWER = AgentProfile(
    role=AgentRole.REVIEWER,
    name="Reviewer",
    system_prompt=(
        "You are a senior code reviewer and security auditor. Review code for bugs, "
        "security vulnerabilities, performance issues, and style violations. Provide "
        "actionable feedback with specific line references. Check for OWASP Top 10, "
        "injection risks, and proper input validation."
    ),
    tools=["file_read", "shell_exec"],
    temperature=0.1,
)

TESTER = AgentProfile(
    role=AgentRole.TESTER,
    name="Tester",
    system_prompt=(
        "You are a QA engineer specializing in test automation. Write comprehensive "
        "unit tests, integration tests, and edge case tests. Aim for >80% coverage. "
        "Generate test data, mock external dependencies, and document test scenarios."
    ),
    tools=["file_read", "file_write", "shell_exec"],
    max_iterations=8,
    temperature=0.3,
)

OPS = AgentProfile(
    role=AgentRole.OPS,
    name="Ops",
    system_prompt=(
        "You are a DevOps engineer. Create deployment configurations, CI/CD pipelines, "
        "Dockerfiles, and infrastructure-as-code. Plan rollout strategies, monitoring "
        "setup, and rollback procedures. Consider cost optimization and security hardening."
    ),
    tools=["file_read", "file_write", "shell_exec"],
    temperature=0.2,
)

AGENT_REGISTRY: dict[AgentRole, AgentProfile] = {
    AgentRole.ARCHITECT: ARCHITECT,
    AgentRole.DEVELOPER: DEVELOPER,
    AgentRole.REVIEWER: REVIEWER,
    AgentRole.TESTER: TESTER,
    AgentRole.OPS: OPS,
}
