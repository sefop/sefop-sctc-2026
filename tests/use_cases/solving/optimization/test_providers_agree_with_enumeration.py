"""Cross-checks that MipHighsSolutionProvider agrees with the brute-force
EnumerationSolutionProvider reference on small instances.

Correctness of the formulation is checked at the observable level only — the
revenue of the returned Load — never by inspecting solver-internal structure.
Which shipments are loaded is not compared: when several loads share the
highest revenue, either provider may return any of them.
"""

import math
import random

import pytest

from domain.flight import Flight
from tests.builders import a_flight, ready_to_solve
from use_cases.solving.optimization.enumeration.enumeration_solution_provider import EnumerationSolutionProvider
from use_cases.solving.optimization.mip_highs.mip_highs_solution_provider import MipHighsSolutionProvider

_HAND_MADE_FLIGHTS = {
    "everything_fits": a_flight(1000, [("S1", "A", 300, 3000), ("S2", "B", 250, 2300), ("S3", "C", 100, 800)]),
    "only_one_fits": a_flight(300, [("S1", "A", 300, 3000), ("S2", "B", 250, 3500), ("S3", "C", 200, 900)]),
    "weight_limit_used_exactly": a_flight(
        500, [("S1", "A", 500, 3000), ("S2", "B", 250, 2000), ("S3", "C", 250, 1800)]
    ),
    "best_revenue_per_kg_is_not_enough": a_flight(
        # S1 earns the most per kg, but taking it wastes capacity: S2 + S3 win.
        100,
        [("S1", "A", 60, 660), ("S2", "B", 50, 500), ("S3", "C", 50, 500)],
    ),
    "several_loads_share_the_best_revenue": a_flight(
        200, [("S1", "A", 200, 1000), ("S2", "B", 200, 1000), ("S3", "C", 100, 500), ("S4", "D", 100, 500)]
    ),
    "fractional_weights_and_revenues": a_flight(
        10.5, [("S1", "A", 3.5, 120.50), ("S2", "B", 4.25, 150.75), ("S3", "C", 6.0, 199.99), ("S4", "D", 2.75, 90.10)]
    ),
}


def _random_flight(seed: int) -> Flight:
    """Build a small random flight. The same seed always gives the same flight."""
    rng = random.Random(seed)
    shipment_count = rng.randint(1, 10)
    shipments = [
        (f"S{i + 1}", f"Customer {rng.randint(1, 4)}", rng.randint(50, 400), rng.randint(200, 4000))
        for i in range(shipment_count)
    ]
    heaviest = max(weight_kg for _, _, weight_kg, _ in shipments)
    total = sum(weight_kg for _, _, weight_kg, _ in shipments)
    # A limit between the heaviest shipment and the total weight keeps every
    # shipment able to fly on its own while usually forcing a real choice.
    return a_flight(rng.randint(heaviest, total), shipments, flight_id=f"RANDOM-{seed}")


@pytest.mark.parametrize("flight", _HAND_MADE_FLIGHTS.values(), ids=_HAND_MADE_FLIGHTS.keys())
def test_the_solver_earns_the_same_revenue_as_trying_every_load_by_hand(flight):
    # ARRANGE
    data = ready_to_solve(flight)

    # ACT
    solved = MipHighsSolutionProvider().solve(data)
    reference = EnumerationSolutionProvider().solve(data)

    # ASSERT
    assert math.isclose(solved.total_revenue_usd, reference.total_revenue_usd)
    assert solved.total_weight_kg <= flight.max_weight_kg


@pytest.mark.parametrize("seed", range(30))
def test_the_solver_earns_the_same_revenue_as_trying_every_load_on_random_flights(seed):
    # ARRANGE
    flight = _random_flight(seed)
    data = ready_to_solve(flight)

    # ACT
    solved = MipHighsSolutionProvider().solve(data)
    reference = EnumerationSolutionProvider().solve(data)

    # ASSERT
    assert math.isclose(solved.total_revenue_usd, reference.total_revenue_usd)
    assert solved.total_weight_kg <= flight.max_weight_kg
