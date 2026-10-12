"""
ROLE: Value Object — packages the outcome of planning a flight for callers.

WHY THIS EXISTS:
    Every call to OptimizeCargo returns an ``OptimizationResponse`` rather
    than a raw ``Load``. This gives callers a uniform object to inspect:
    check ``outcome``, read the ``load`` on success, or read the ``message``
    otherwise — no exception handling required.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from domain.flight import Flight
from domain.load import Load


class Outcome(Enum):
    """The three ways planning a flight can end, each named for the planner.

    Attributes:
        LOADED: A load was chosen. This is the normal result.
        NO_SHIPMENT_FITS: The data is valid, but every shipment alone weighs
            more than the aircraft can carry, so nothing can fly.
        INVALID_INPUT: The flight's data is missing or wrong, so no decision
            was attempted. The planner has to correct the data first.
    """

    LOADED = "LOADED"
    NO_SHIPMENT_FITS = "NO_SHIPMENT_FITS"
    INVALID_INPUT = "INVALID_INPUT"


@dataclass(frozen=True)
class OptimizationResponse:
    """Output of the "optimize cargo" use case.

    Attributes:
        outcome: Which of the three outcomes occurred.
        flight: The flight that was planned, or None when its data could not
            be read.
        load: The chosen load, present only when outcome is LOADED.
        message: Explanation of what is wrong with the input, present only
            when outcome is INVALID_INPUT.
    """

    outcome: Outcome
    flight: Flight | None
    load: Load | None
    message: str | None

    @classmethod
    def loaded(cls, load: Load) -> "OptimizationResponse":
        """Build the normal response: a load was chosen for the flight.

        Args:
            load: The load to recommend to the planner.

        Returns:
            An OptimizationResponse with outcome LOADED.
        """
        return cls(outcome=Outcome.LOADED, flight=load.flight, load=load, message=None)

    @classmethod
    def no_shipment_fits(cls, flight: Flight) -> "OptimizationResponse":
        """Build the response for a valid flight on which nothing can fly.

        Args:
            flight: The flight whose shipments are all too heavy.

        Returns:
            An OptimizationResponse with outcome NO_SHIPMENT_FITS and no load.
        """
        return cls(outcome=Outcome.NO_SHIPMENT_FITS, flight=flight, load=None, message=None)

    @classmethod
    def invalid_input(cls, message: str) -> "OptimizationResponse":
        """Build the response for flight data that is missing or wrong.

        Args:
            message: What is wrong, in words the planner can act on.

        Returns:
            An OptimizationResponse with outcome INVALID_INPUT and no load.
        """
        return cls(outcome=Outcome.INVALID_INPUT, flight=None, load=None, message=message)
