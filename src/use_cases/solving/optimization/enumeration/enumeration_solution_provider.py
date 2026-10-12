"""
ROLE: Implementation — of SolutionProvider, using exhaustive search rather than
any solver library. Brute-force and exact; used as the reference in tests.

WHY THIS EXISTS:
    Every possible set of shipments is tried; the set with the highest total
    revenue that respects the weight limit wins. This is simple enough to
    trust by inspection, which is exactly why it serves as the ground truth
    MipHighsSolutionProvider is checked against in tests, instead of asserting
    on that provider's internal formulation.

    The program itself does not solve with this provider: with n shipments
    there are 2^n sets to try, which stops being practical well before a
    real flight's worth of cargo.
"""

from __future__ import annotations

import itertools

from domain.load import Load
from use_cases.solving.optimization.solution_provider import SolutionProvider
from use_cases.solving.preprocessing.pre_processed_data import PreProcessedData


class EnumerationSolutionProvider(SolutionProvider):
    """Tries every set of shipments and keeps the one with the highest revenue.

    Feasibility is delegated entirely to Load.__post_init__'s existing
    weight-limit validation rather than reimplemented here: a set of
    shipments is feasible if and only if constructing a Load from it doesn't
    raise ValueError. This keeps the one weight check in the codebase in one
    place, instead of two implementations that could silently drift apart.
    """

    @property
    def name(self) -> str:
        return "Brute-force Enumeration"

    def solve(self, data: PreProcessedData) -> Load | None:
        """Exhaustively search every set of shipments.

        Args:
            data: The preprocessed flight and the shipments that can fly.

        Returns:
            A Load with the highest total revenue. Never None: loading
            nothing is always possible.
        """
        flight = data.flight
        best = Load(flight=flight, loaded=[])
        # Each shipment either flies (True) or is left behind (False), so the
        # search space is every True/False combination across the shipments.
        for decisions in itertools.product([False, True], repeat=len(data.feasible_shipments)):
            loaded = [shipment for shipment, flies in zip(data.feasible_shipments, decisions) if flies]
            try:
                candidate = Load(flight=flight, loaded=loaded)
            except ValueError:
                continue
            # Strict '>' (not '>=') means the first-enumerated set wins any
            # tie. Ties are not otherwise handled: any highest-revenue load
            # is an acceptable answer.
            if candidate.total_revenue_usd > best.total_revenue_usd:
                best = candidate

        return best
