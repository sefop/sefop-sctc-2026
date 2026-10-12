"""Data container that carries flight data into a SolutionProvider.

Defines the boundary between the preprocessing stage and the SolutionProvider
stage. Keeping them separate makes each independently extensible.
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.flight import Flight
from domain.shipment import Shipment


@dataclass(frozen=True)
class PreProcessedData:
    """Preprocessed data ready for a SolutionProvider to run on.

    Attributes:
        flight: The original flight to plan.
        feasible_shipments: Shipments that fit within the weight limit on
            their own. SolutionProvider implementations should iterate this
            list instead of flight.shipments to avoid wasting effort on
            shipments that can never fly.
    """

    flight: Flight
    feasible_shipments: list[Shipment]
