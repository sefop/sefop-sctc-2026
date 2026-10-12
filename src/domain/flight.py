"""
ROLE: Value Object — one flight to plan: its weight limit and the shipments waiting for it.

WHY THIS EXISTS:
    A Flight bundles everything a SolutionProvider needs to run - the weight limit and the
    shipments competing for it - into a single, validated unit. Downstream code (use_cases,
    solving providers) can accept a Flight without re-checking its contents, because an invalid
    Flight can never be constructed in the first place.
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.shipment import Shipment


@dataclass(frozen=True)
class Flight:
    """One instance of the cargo decision: which shipments fly within the weight limit.

    This is a frozen (immutable) value object. Constructing a Flight runs all validation
    immediately, so any code that later receives a Flight instance can trust that its limit is
    positive and its shipment list is well-formed, without re-validating.

    Attributes:
        flight_id: Identifier of the flight, shown to the planner in the output.
        max_weight_kg: Maximum total weight of cargo the aircraft can carry, in kilograms.
            This is a physical limit: no load may ever exceed it.
        shipments: Non-empty list of shipments waiting for this flight. Ids must be unique
            within the list, since Shipment.id is how the planner tells shipments apart.
    """

    flight_id: str
    max_weight_kg: float
    shipments: list[Shipment]

    def __post_init__(self) -> None:
        if not self.flight_id:
            raise ValueError("the flight needs an id")
        if self.max_weight_kg <= 0:
            raise ValueError(f"the weight limit is {self.max_weight_kg} kg; it must be greater than 0")
        if not self.shipments:
            raise ValueError("the flight has no shipments to choose from")
        seen: set[str] = set()
        for shipment in self.shipments:
            # A repeated id would make a shipment ambiguous in the planner's table, so it is
            # rejected here rather than left for downstream code to discover.
            if shipment.id in seen:
                raise ValueError(f"shipment id '{shipment.id}' appears more than once")
            seen.add(shipment.id)
