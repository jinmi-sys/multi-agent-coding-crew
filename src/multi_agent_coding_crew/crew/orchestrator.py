"""Crew orchestrator - manages multi-agent collaboration."""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from ..agents.definitions import AgentRole, AGENT_REGISTRY
from ..agents.executor import AgentExecutor, AgentResult


class PipelinePhase(Enum):
    REQUIREMENTS = "requirements"
    DESIGN = "design"
    IMPLEMENTATION = "implementation"
    REVIEW = "review"
    TESTING = "testing"
    DEPLOYMENT = "deployment"


PHASE_ORDER = [
    PipelinePhase.REQUIREMENTS,
    PipelinePhase.DESIGN,
    PipelinePhase.IMPLEMENTATION,
    PipelinePhase.REVIEW,
    PipelinePhase.TESTING,
    PipelinePhase.DEPLOYMENT,
]

PHASE_AGENTS: dict[PipelinePhase, list[AgentRole]] = {
    PipelinePhase.REQUIREMENTS: [AgentRole.ARCHITECT],
    PipelinePhase.DESIGN: [AgentRole.ARCHITECT],
    PipelinePhase.IMPLEMENTATION: [AgentRole.DEVELOPER],
    PipelinePhase.REVIEW: [AgentRole.REVIEWER],
    PipelinePhase.TESTING: [AgentRole.TESTER],
    PipelinePhase.DEPLOYMENT: [AgentRole.OPS],
}


@dataclass
class PhaseResult:
    phase: PipelinePhase
    agent_results: list[AgentResult] = field(default_factory=list)
    duration_sec: float = 0.0
    success: bool = True

    @property
    def output(self) -> str:
        return "\n\n".join(r.output for r in self.agent_results if r.output)


@dataclass
class CrewRun:
    """Full run of the coding crew pipeline."""
    task: str
    phases: list[PhaseResult] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None

    @property
    def duration(self) -> float:
        end = self.end_time or time.time()
        return end - self.start_time

    @property
    def success(self) -> bool:
        return all(p.success for p in self.phases)

    def summary(self) -> dict:
        return {
            "task": self.task[:200],
            "phases": len(self.phases),
            "success": self.success,
            "duration_sec": round(self.duration, 2),
            "total_tokens": sum(
                r.token_usage for p in self.phases for r in p.agent_results
            ),
        }


class CrewOrchestrator:
    """Orchestrates multi-agent SDLC pipeline."""

    def __init__(self, mimo_endpoint: str = "http://localhost:11434"):
        self.endpoint = mimo_endpoint
        self.executors: dict[AgentRole, AgentExecutor] = {}
        self._init_executors()

    def _init_executors(self) -> None:
        for role, profile in AGENT_REGISTRY.items():
            self.executors[role] = AgentExecutor(profile, self.endpoint)

    def run(self, task: str, phases: Optional[list[PipelinePhase]] = None) -> CrewRun:
        """Execute full SDLC pipeline for a task."""
        run = CrewRun(task=task)
        target_phases = phases or PHASE_ORDER
        context = f"Task: {task}"

        for phase in target_phases:
            phase_result = self._run_phase(phase, context)
            run.phases.append(phase_result)
            context += f"\n\n--- {phase.value.upper()} Output ---\n{phase_result.output}"
            if not phase_result.success:
                break

        run.end_time = time.time()
        return run

    def _run_phase(self, phase: PipelinePhase, context: str) -> PhaseResult:
        """Run a single pipeline phase."""
        result = PhaseResult(phase=phase)
        start = time.time()
        agents = PHASE_AGENTS.get(phase, [])

        for role in agents:
            executor = self.executors.get(role)
            if not executor:
                continue
            task_prompt = self._build_phase_prompt(phase)
            agent_result = executor.run(task_prompt, context)
            result.agent_results.append(agent_result)
            if not agent_result.success:
                result.success = False

        result.duration_sec = time.time() - start
        return result

    @staticmethod
    def _build_phase_prompt(phase: PipelinePhase) -> str:
        prompts = {
            PipelinePhase.REQUIREMENTS: "Analyze the task requirements. Identify functional and non-functional requirements. List assumptions and constraints.",
            PipelinePhase.DESIGN: "Design the system architecture. Define modules, interfaces, data flow, and tech stack. Output a structured design document.",
            PipelinePhase.IMPLEMENTATION: "Implement the code based on the architecture design. Write clean, documented, production-ready code.",
            PipelinePhase.REVIEW: "Review the implementation for bugs, security issues, and code quality. Provide specific feedback with line references.",
            PipelinePhase.TESTING: "Write comprehensive tests. Cover unit tests, integration tests, and edge cases. Report estimated coverage.",
            PipelinePhase.DEPLOYMENT: "Create deployment configuration. Plan CI/CD pipeline, containerization, monitoring, and rollback strategy.",
        }
        return prompts.get(phase, "Execute this phase.")
