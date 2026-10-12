"""
ROLE: Value Object — a validated answer to a Flight: which shipments fly.

WHY THIS EXISTS:
    A Load pairs the shipments chosen to fly with the Flight they answer, and derives the
    resulting totals itself. Deriving the totals here - rather than trusting a caller to compute
    and pass them in - means a Load can never report totals that disagree with its own shipments,
    and can never exist in a state that exceeds the aircraft's weight limit.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from domain.flight import Flight
from domain.shipment import Shipment


@dataclass(frozen=True)
class Load:
    """A candidate decision for a Flight: the shipments that fly; the rest are left behind.

    This is a frozen (immutable) value object whose left_behind, total_revenue_usd and
    total_weight_kg fields are *computed*, not supplied by the caller. They are declared with
    ``field(init=False)`` so the constructor only accepts flight and loaded; __post_init__ then
    derives the rest and uses ``object.__setattr__`` to set them - the one sanctioned way to
    assign a field on a frozen dataclass. The same __post_init__ call also checks the total
    weight against the Flight's limit, so an overweight Load can never be constructed.

    An empty Load is valid: loading nothing never exceeds the weight limit.

    Attributes:
        flight: The Flight this load answers.
        loaded: Shipments that fly. Each must be one of flight.shipments, at most once.
        left_behind: Every shipment of the flight that does not fly, in the flight's order,
            derived automatically.
        total_revenue_usd: Sum of revenue across the loaded shipments, derived automatically.
        total_weight_kg: Sum of weight across the loaded shipments, derived automatically.
            Must not exceed flight.max_weight_kg.
    """

    flight: Flight
    loaded: list[Shipment]
    left_behind: list[Shipment] = field(init=False)
    total_revenue_usd: float = field(init=False)
    total_weight_kg: float = field(init=False)

    def __post_init__(self) -> None:
        on_flight = {shipment.id for shipment in self.flight.shipments}
        loaded_ids: set[str] = set()
        for shipment in self.loaded:
            if shipment.id not in on_flight:
                raise ValueError(f"shipment '{shipment.id}' is not on flight '{self.flight.flight_id}'")
            if shipment.id in loaded_ids:
                raise ValueError(f"shipment '{shipment.id}' is loaded more than once")
            loaded_ids.add(shipment.id)
        left_behind = [shipment for shipment in self.flight.shipments if shipment.id not in loaded_ids]
        revenue = sum(shipment.revenue_usd for shipment in self.loaded)
        weight = sum(shipment.weight_kg for shipment in self.loaded)
        # object.__setattr__ bypasses the frozen dataclass's usual "no attribute assignment"
        # restriction. This is safe only here, inside __post_init__, before the instance is
        # ever exposed to callers.
        object.__setattr__(self, "left_behind", left_behind)
        object.__setattr__(self, "total_revenue_usd", revenue)
        object.__setattr__(self, "total_weight_kg", weight)
        # The aircraft's weight limit is a hard physical limit. Checking it here, in the one
        # place every Load passes through, means no part of the program can produce or print
        # an overweight load.
        if weight > self.flight.max_weight_kg:
            raise ValueError(f"total weight {weight} kg exceeds the weight limit {self.flight.max_weight_kg} kg")
