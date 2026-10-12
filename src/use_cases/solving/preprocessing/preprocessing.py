"""Preprocessing stage that prepares flight data for a SolutionProvider.

Domain validation (Flight.__post_init__) already guarantees that each shipment
has positive weight and revenue and that ids are unique. Preprocessing goes one
step further: it sets aside shipments that can never appear in any load.

A shipment is *oversize* if it alone already weighs more than the aircraft's
weight limit. No SolutionProvider could ever load such a shipment, so setting
it aside here shrinks the problem before any solver sees it.
"""

from __future__ import annotations

from domain.flight import Flight
from use_cases.solving.preprocessing.pre_processed_data import PreProcessedData


class PreProcess:
    """Preprocessing step before a SolutionProvider runs.

    Sets aside oversize shipments, then wraps the remaining data in
    PreProcessedData for the SolutionProvider stage.
    """

    def run(self, flight: Flight) -> PreProcessedData:
        """Set aside oversize shipments and prepare data for the SolutionProvider stage.

        Args:
            flight: The validated flight to plan.

        Returns:
            PreProcessedData with feasible_shipments containing only the
            shipments that fit within the weight limit on their own.
        """
        feasible_shipments = [s for s in flight.shipments if s.weight_kg <= flight.max_weight_kg]
        return PreProcessedData(flight=flight, feasible_shipments=feasible_shipments)
