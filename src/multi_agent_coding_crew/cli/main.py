"""CLI entry point for multi-agent-coding-crew."""

import json
import sys
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


@click.group()
def cli():
    """Multi-Agent Coding Crew - Autonomous SDLC Terminal."""
    pass


@cli.command()
@click.argument("task")
@click.option("--endpoint", default="http://localhost:11434", help="MiMo API endpoint")
@click.option("--phases", default=None, help="Comma-separated phases to run")
@click.option("--output", "-o", default=None, help="Output file path")
def new(task: str, endpoint: str, phases: str | None, output: str | None):
    """Start a new coding crew run."""
    from ..crew.orchestrator import CrewOrchestrator, PipelinePhase

    console.print(Panel(f"[bold]Task:[/bold] {task}", title="Starting Crew"))

    phase_list = None
    if phases:
        phase_list = [PipelinePhase(p.strip()) for p in phases.split(",")]

    orchestrator = CrewOrchestrator(mimo_endpoint=endpoint)
    run = orchestrator.run(task, phases=phase_list)

    for phase_result in run.phases:
        status = "[green]OK" if phase_result.success else "[red]FAIL"
        console.print(f"  {status}[/] {phase_result.phase.value} ({phase_result.duration_sec:.1f}s)")

    summary = run.summary()
    console.print(Panel(json.dumps(summary, indent=2), title="Run Summary"))

    if output:
        from ..utils.export import export_json
        export_json(summary, output)
        console.print(f"Exported to {output}")


@cli.command()
def agents():
    """List available agents."""
    from ..agents.definitions import AGENT_REGISTRY

    table = Table(title="Coding Crew Agents")
    table.add_column("Role", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Tools", style="yellow")

    for role, profile in AGENT_REGISTRY.items():
        table.add_row(role.value, profile.name, ", ".join(profile.tools))

    console.print(table)


@cli.command()
def phases():
    """List pipeline phases."""
    from ..crew.orchestrator import PHASE_ORDER, PHASE_AGENTS

    table = Table(title="Pipeline Phases")
    table.add_column("Phase", style="cyan")
    table.add_column("Agents", style="green")

    for phase in PHASE_ORDER:
        agents = [a.value for a in PHASE_AGENTS.get(phase, [])]
        table.add_row(phase.value, ", ".join(agents))

    console.print(table)


if __name__ == "__main__":
    cli()
