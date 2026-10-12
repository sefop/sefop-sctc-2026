"""Small helpers that build domain objects for tests in one readable line."""

from __future__ import annotations

from domain.flight import Flight
from domain.shipment import Shipment
from use_cases.solving.preprocessing.pre_processed_data import PreProcessedData


def a_flight(max_weight_kg: float, shipments: list[tuple[str, str, float, float]], flight_id: str = "TEST") -> Flight:
    """Build a Flight from (id, customer, weight_kg, revenue_usd) tuples."""
    return Flight(
        flight_id=flight_id,
        max_weight_kg=max_weight_kg,
        shipments=[
            Shipment(id=id_, customer=customer, weight_kg=weight_kg, revenue_usd=revenue_usd)
            for id_, customer, weight_kg, revenue_usd in shipments
        ],
    )


def ready_to_solve(flight: Flight) -> PreProcessedData:
    """Wrap a Flight whose shipments all fit on their own, as preprocessing would."""
    return PreProcessedData(flight=flight, feasible_shipments=list(flight.shipments))


def loaded_ids(load) -> list[str]:
    """Ids of the shipments that fly, for compact assertions."""
    return [shipment.id for shipment in load.loaded]
