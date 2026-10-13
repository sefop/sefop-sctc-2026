"""
ROLE: Value Object — what the preprocessing stage hands to a SolutionProvider.

WHY THIS EXISTS:
    Preprocessing and solving are separate stages, and this is the one thing
    passed between them. Giving that hand-over its own type means a new
    preprocessing step (or a new solver) only has to agree on this object, not
    on how the other stage works inside.
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.flight import Flight
from domain.shipment import Shipment


@dataclass(frozen=True)
class PreProcessedData:
    """Preprocessed data ready for a SolutionProvider to run on.

    This is a frozen dataclass: once built it cannot be changed, so a
    SolutionProvider cannot alter by accident the data another stage relies on.

    Attributes:
        flight: The original flight to plan.
        feasible_shipments: Shipments that fit within the weight limit on
            their own. SolutionProvider implementations should iterate this
            list instead of flight.shipments to avoid wasting effort on
            shipments that can never fly.
    """

    flight: Flight
    feasible_shipments: list[Shipment]
