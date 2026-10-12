"""Orchestrates the full "optimize cargo" use case.

This is the application-layer entry point that calling code (cli.py) uses to
plan one flight: choose the shipments that fly so that revenue is as high as
possible without exceeding the aircraft's weight limit. It coordinates loading
data and running the solving pipeline, so callers don't need to manage those
steps themselves.
"""

from __future__ import annotations

import logging

from use_cases.optimization_response import OptimizationResponse
from use_cases.ports.base_data_loader import BaseDataLoader
from use_cases.solving.orchestrator import Orchestrator

logger = logging.getLogger(__name__)


class OptimizeCargo:
    """Runs the "load -> optimize -> respond" pipeline for one flight.

    Both collaborators are constructor-injected (Dependency Injection): this
    class only coordinates them, it never builds its own BaseDataLoader or
    Orchestrator. That keeps this use case free to work with any data source
    or solving pipeline the caller (startup.py) assembles, and lets tests
    substitute either one without touching this class.
    """

    def __init__(self, flight_loader: BaseDataLoader, orchestrator: Orchestrator) -> None:
        self._flight_loader = flight_loader
        self._orchestrator = orchestrator

    def optimize(self, flight_id: str) -> OptimizationResponse:
        """Load a flight and choose the shipments that fly.

        Args:
            flight_id: Identifier of the flight to plan.

        Returns:
            An OptimizationResponse carrying one of three outcomes: a load,
            "no shipment fits", or an explanation of what is wrong with the
            flight's data.
        """
        logger.info("Planning flight: %s", flight_id)

        # Wrong or missing data is an expected outcome, not a crash: the
        # planner gets an explanation they can act on instead of a traceback.
        try:
            flight = self._flight_loader.load(flight_id)
        except ValueError as exc:
            logger.info("Invalid data for flight %s: %s", flight_id, exc)
            return OptimizationResponse.invalid_input(str(exc))
        if flight is None:
            logger.info("Flight not found: %s", flight_id)
            return OptimizationResponse.invalid_input(f"no data was found for flight '{flight_id}'")

        load = self._orchestrator.solve(flight)
        if load is None:
            logger.info("No shipment fits on flight: %s", flight_id)
            return OptimizationResponse.no_shipment_fits(flight)

        logger.info("Flight %s planned", flight_id)
        return OptimizationResponse.loaded(load)
