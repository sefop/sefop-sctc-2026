"""
ROLE: Composition root — holds the settings and assembles the program's parts.

WHY THIS EXISTS:
    This module has two jobs, kept together because they are two sides of the
    same coin:

    1. Hold every configurable value (the `Settings` dataclass) in one place,
       rather than scattered as literal strings across the codebase.
    2. Assemble the objects the command line needs (the `build_*` functions).
       This is the only module allowed to import concrete adapters and build
       concrete use cases. cli.py calls these functions instead of building
       anything itself, so every other module can depend on abstract ports
       (use_cases/ports/) without knowing which concrete adapter is wired in.

    The consequence: to read flights from a database, or to use another
    solver, this is the one file that changes.
"""

from __future__ import annotations

from dataclasses import dataclass

from adapters.console_result_writer import ConsoleResultWriter
from adapters.json_data_loader import JsonDataLoader
from use_cases.ports.base_result_writer import BaseResultWriter
from use_cases.solving.optimization.mip_highs.mip_highs_solution_provider import MipHighsSolutionProvider
from use_cases.solving.orchestrator import Orchestrator
from use_cases.solving.postprocessing.postprocessing import PostProcess
from use_cases.solving.preprocessing.preprocessing import PreProcess
from use_cases.use_case_optimize_cargo import OptimizeCargo


@dataclass
class Settings:
    """Holds all configurable values for the application.

    Attributes:
        folder_path: Root directory where flight subfolders live
            (data/SC101/data.json, data/SC001/data.json, …).
        show_solver_log: Whether the solver prints its own progress log to
            the console, above the planner's table.
    """

    folder_path: str = "data"
    show_solver_log: bool = False


def build_orchestrator(settings: Settings) -> Orchestrator:
    """Assemble an Orchestrator with all of its solving-pipeline collaborators.

    This is the one place in the codebase where the solver technology is
    chosen. Using a different solver means writing a new SolutionProvider and
    changing the one line below — nothing else in the codebase needs to change.

    Args:
        settings: Application settings; show_solver_log decides whether the
            solver's own log is printed.

    Returns:
        A fully wired Orchestrator, ready to plan a Flight.
    """
    return Orchestrator(
        preprocessing=PreProcess(),
        postprocessing=PostProcess(),
        solution_provider=MipHighsSolutionProvider(show_solver_log=settings.show_solver_log),
    )


def build_optimize_cargo(settings: Settings) -> OptimizeCargo:
    """Assemble an OptimizeCargo use case.

    Args:
        settings: Application settings; folder_path is where flight data is
            loaded from, show_solver_log is passed on to the solver.

    Returns:
        A fully wired OptimizeCargo, ready to plan one flight id.
    """
    return OptimizeCargo(
        flight_loader=JsonDataLoader(folder_path=settings.folder_path),
        orchestrator=build_orchestrator(settings),
    )


def build_result_writer() -> BaseResultWriter:
    """Select the concrete BaseResultWriter that presents outcomes to the planner.

    Returns:
        A ConsoleResultWriter printing to the terminal.
    """
    return ConsoleResultWriter()
