"""
ROLE: Orchestrator — sequences the cargo optimization pipeline end-to-end.

WHY THIS EXISTS:
    The Orchestrator is the public face of the use case's internal solving
    pipeline (this whole `solving/` subpackage is an implementation detail of
    `OptimizeCargo`, not a top-level architecture layer). Given a Flight, it
    runs three explicit stages: preprocessing -> solving -> postprocessing,
    announcing each one in the log as it starts. Returns a Load or None.
    Callers never need to know which provider ran or how
    preprocessing/postprocessing work.
"""

from __future__ import annotations

import logging

from domain.flight import Flight
from domain.load import Load
from use_cases.solving.optimization.solution_provider import SolutionProvider
from use_cases.solving.postprocessing.postprocessing import PostProcess
from use_cases.solving.preprocessing.preprocessing import PreProcess
from use_cases.stage_log import log_stage

logger = logging.getLogger(__name__)


class Orchestrator:
    """Runs preprocessing, a solution provider and postprocessing for a Flight.

    Every collaborator is constructor-injected (Dependency Injection) rather
    than built here, so a fork can swap any stage — or test this class with
    fakes — without editing this file. In particular, Orchestrator only ever
    sees the abstract SolutionProvider type: it has no idea which solver
    technology is behind solution_provider.
    """

    def __init__(
        self,
        preprocessing: PreProcess,
        postprocessing: PostProcess,
        solution_provider: SolutionProvider,
    ) -> None:
        self._preprocessing = preprocessing
        self._postprocessing = postprocessing
        self._solution_provider = solution_provider

    def solve(self, flight: Flight) -> Load | None:
        """Run the full optimization pipeline.

        Args:
            flight: The flight to plan.

        Returns:
            A Load with the highest total revenue, or None if no shipment can
            fly at all.

        Raises:
            RuntimeError: If the solution provider fails to produce a load.
                Loading nothing is always possible, so a provider that
                returns no load has malfunctioned; that must not be reported
                to the planner as "no shipment fits".
        """
        log_stage(logger, "Preprocess")
        data = self._preprocessing.run(flight)
        can_fly = len(data.feasible_shipments)
        logger.info("%d %s can fly", can_fly, "shipment" if can_fly == 1 else "shipments")
        logger.info("%d set aside (heavier than the limit)", len(flight.shipments) - can_fly)
        if not data.feasible_shipments:
            # Every shipment alone weighs more than the aircraft can carry,
            # so there is no decision to make.
            return None

        log_stage(logger, "Solve")
        logger.info("Solver: %s", self._solution_provider.name)
        load = self._solution_provider.solve(data)
        if load is None:
            raise RuntimeError(f"{self._solution_provider.name} did not return a load")

        log_stage(logger, "Postprocess")
        load = self._postprocessing.run(load)
        loaded = len(load.loaded)
        logger.info("%d %s loaded, in flight order", loaded, "shipment" if loaded == 1 else "shipments")
        return load
