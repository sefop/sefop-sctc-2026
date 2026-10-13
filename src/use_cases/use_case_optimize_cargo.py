"""
ROLE: Orchestrator — runs the "optimize cargo" use case for one flight.

WHY THIS EXISTS:
    A use case is one thing the planner asks the program to do. This one is
    "choose the shipments that fly so that revenue is as high as possible
    without exceeding the aircraft's weight limit". The module coordinates
    reading the flight and running the solving pipeline, and turns whatever
    happens into one of three outcomes, so the caller (cli.py) deals with a
    single call and a single answer.

    It contains no rule of its own: what makes a flight valid lives in
    domain/, and how a load is chosen lives in use_cases/solving/.
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

        Each stage is announced in the log as it starts, so whoever watches
        the console can follow the run.

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
        # ",.10g" writes 1000.0 as "1,000" and 350.5 as "350.5": thousands
        # separators, and decimals only when the weight has them.
        logger.info("Flight %s, weight limit %s kg", flight.flight_id, f"{flight.max_weight_kg:,.10g}")
        logger.info("%s from %s", _count(len(flight.shipments), "shipment"), _count(len(customers), "customer"))

        load = self._orchestrator.solve(flight)
        if load is None:
            return OptimizationResponse.no_shipment_fits(flight)

        return OptimizationResponse.loaded(load)


def _count(number: int, noun: str) -> str:
    """Word a count: "1 shipment", "9 shipments"."""
    return f"{number} {noun}" if number == 1 else f"{number} {noun}s"
