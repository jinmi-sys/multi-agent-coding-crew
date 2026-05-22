"""Agent execution loop - processes tasks via MiMo API."""

import json
import time
from dataclasses import dataclass, field
from typing import Any, Optional

from .definitions import AgentProfile, AgentRole, AGENT_REGISTRY


@dataclass
class AgentMessage:
    role: str  # "system", "user", "assistant"
    content: str
    timestamp: float = field(default_factory=time.time)
    agent: Optional[str] = None


@dataclass
class AgentResult:
    agent: AgentRole
    output: str
    artifacts: list[dict[str, Any]] = field(default_factory=list)
    iterations: int = 0
    token_usage: int = 0
    success: bool = True
    error: Optional[str] = None


class AgentExecutor:
    """Executes a single agent turn with tool calling loop."""

    def __init__(self, profile: AgentProfile, mimo_endpoint: str = "http://localhost:11434"):
        self.profile = profile
        self.endpoint = mimo_endpoint
        self.messages: list[AgentMessage] = []
        self.tools_available: dict[str, Any] = {}

    def register_tools(self, tools: dict[str, Any]) -> None:
        self.tools_available.update(tools)

    def _build_system_prompt(self, context: str = "") -> str:
        parts = [self.profile.system_prompt]
        if context:
            parts.append(f"\n--- Project Context ---\n{context}")
        if self.tools_available:
            tool_names = ", ".join(self.tools_available.keys())
            parts.append(f"\n--- Available Tools ---\n{tool_names}")
        return "\n".join(parts)

    def run(self, task: str, context: str = "") -> AgentResult:
        """Execute task with iterative tool-calling loop."""
        system_msg = AgentMessage(role="system", content=self._build_system_prompt(context))
        user_msg = AgentMessage(role="user", content=task, agent="user")

        self.messages = [system_msg, user_msg]
        artifacts = []
        total_tokens = 0

        for iteration in range(self.profile.max_iterations):
            response = self._call_mimo()
            total_tokens += response.get("tokens", 0)
            assistant_content = response.get("content", "")

            tool_calls = self._extract_tool_calls(assistant_content)
            if not tool_calls:
                return AgentResult(
                    agent=self.profile.role,
                    output=assistant_content,
                    artifacts=artifacts,
                    iterations=iteration + 1,
                    token_usage=total_tokens,
                )

            for call in tool_calls:
                tool_name = call.get("tool")
                tool_args = call.get("args", {})
                if tool_name in self.tools_available:
                    result = self.tools_available[tool_name](**tool_args)
                    artifacts.append({"tool": tool_name, "args": tool_args, "result": result})
                    self.messages.append(
                        AgentMessage(role="user", content=f"Tool {tool_name} result: {result}", agent="tool")
                    )

        return AgentResult(
            agent=self.profile.role,
            output=self.messages[-1].content if self.messages else "",
            artifacts=artifacts,
            iterations=self.profile.max_iterations,
            token_usage=total_tokens,
            success=False,
            error="Max iterations reached",
        )

    def _call_mimo(self) -> dict[str, Any]:
        """Call MiMo API. Placeholder - integrate with actual endpoint."""
        # In production: httpx.post(self.endpoint, json=payload)
        return {"content": "Agent output placeholder", "tokens": 0}

    @staticmethod
    def _extract_tool_calls(text: str) -> list[dict[str, Any]]:
        """Extract tool call blocks from agent output."""
        calls = []
        if "```tool" not in text:
            return calls
        parts = text.split("```tool")
        for part in parts[1:]:
            block = part.split("```")[0].strip()
            try:
                calls.append(json.loads(block))
            except json.JSONDecodeError:
                continue
        return calls
