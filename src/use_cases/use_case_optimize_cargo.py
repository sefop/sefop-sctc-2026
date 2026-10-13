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
from use_cases.stage_log import log_stage

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
        log_stage(logger, "Read data")

        # Wrong or missing data is an expected outcome, not a crash: the
        # planner gets an explanation they can act on instead of a traceback.
        try:
            flight = self._flight_loader.load(flight_id)
        except ValueError as exc:
            return OptimizationResponse.invalid_input(str(exc))
        if flight is None:
            return OptimizationResponse.invalid_input(f"no data was found for flight '{flight_id}'")

        customers = {shipment.customer for shipment in flight.shipments}
        logger.info("Flight %s, weight limit %s kg", flight.flight_id, f"{flight.max_weight_kg:,.10g}")
        logger.info("%s from %s", _count(len(flight.shipments), "shipment"), _count(len(customers), "customer"))

        load = self._orchestrator.solve(flight)
        if load is None:
            return OptimizationResponse.no_shipment_fits(flight)

        return OptimizationResponse.loaded(load)


def _count(number: int, noun: str) -> str:
    """Word a count: "1 shipment", "9 shipments"."""
    return f"{number} {noun}" if number == 1 else f"{number} {noun}s"
