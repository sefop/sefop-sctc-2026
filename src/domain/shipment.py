"""
ROLE: Entity — one piece of cargo a customer wants on the flight.

WHY THIS EXISTS:
    Shipment has no dependencies on any other layer (use_cases, adapters, solving). Keeping it
    dependency-free means every other layer can depend on Shipment without risking a circular
    import, and the entity can be tested or reused in isolation from the rest of the program.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Shipment:
    """A shipment that either flies or is left behind, with its weight and the revenue it earns.

    This is a frozen (immutable) dataclass: once created, a Shipment cannot be modified.
    Validation runs once, in __post_init__, so an invalid Shipment can never exist; callers
    never need to re-check these fields later.

    Attributes:
        id: Unique, human-readable identifier of the shipment on its flight.
        customer: Name of the customer the shipment belongs to. The planner sees it in the
            output, but it plays no part in deciding what flies: the decision looks only
            at revenue and weight.
        weight_kg: Weight in kilograms. Must be strictly positive.
        revenue_usd: Revenue earned if the shipment flies, in US dollars. Must be strictly
            positive.
    """

    id: str
    customer: str
    weight_kg: float
    revenue_usd: float

    def __post_init__(self) -> None:
        # Fail fast: reject an invalid Shipment at construction time rather than letting
        # a weightless or negative-revenue shipment silently distort the decision later.
        # Messages are written for the planner, who is the one able to correct the data.
        if not self.id:
            raise ValueError("every shipment needs an id")
        if not self.customer:
            raise ValueError(f"shipment '{self.id}' has no customer")
        if self.weight_kg <= 0:
            raise ValueError(f"shipment '{self.id}' has weight {self.weight_kg} kg; weight must be greater than 0")
        if self.revenue_usd <= 0:
            raise ValueError(f"shipment '{self.id}' has revenue {self.revenue_usd} USD; revenue must be greater than 0")
