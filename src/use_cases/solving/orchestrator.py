"""
ROLE: Orchestrator — sequences the cargo optimization pipeline end-to-end.

WHY THIS EXISTS:
    The Orchestrator is the public face of the use case's internal solving
    pipeline (this whole `solving/` subpackage is an implementation detail of
    `OptimizeCargo`, not a top-level architecture layer). Given a Flight, it
    runs three explicit stages: preprocessing -> solving -> postprocessing.
    Returns a Load or None. Callers never need to know which provider ran or
    how preprocessing/postprocessing work.
"""

from __future__ import annotations

import logging

from domain.flight import Flight
from domain.load import Load
from use_cases.solving.optimization.solution_provider import SolutionProvider
from use_cases.solving.postprocessing.postprocessing import PostProcess
from use_cases.solving.preprocessing.preprocessing import PreProcess

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
        """
        data = self._preprocessing.run(flight)
        if not data.feasible_shipments:
            # Every shipment alone weighs more than the aircraft can carry,
            # so there is no decision to make.
            logger.info("No shipment fits within the weight limit; skipping solve")
            return None
        logger.info("Solving with provider: %s", self._solution_provider.name)
        load = self._solution_provider.solve(data)
        if load is None:
            return None
        return self._postprocessing.run(load)
