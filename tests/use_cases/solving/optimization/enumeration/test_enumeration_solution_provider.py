"""Hand-checkable cases for the brute-force reference.

Every other provider is trusted because it agrees with this one, so this one
is checked against answers small enough to verify with pencil and paper.
"""

from tests.builders import a_flight, loaded_ids, ready_to_solve
from use_cases.solving.optimization.enumeration.enumeration_solution_provider import EnumerationSolutionProvider


def test_everything_flies_when_everything_fits():
    # ARRANGE — 300 + 250 = 550 kg on a 1000 kg flight
    flight = a_flight(1000, [("S1", "Atlas Steel", 300, 3000), ("S2", "Bighorn Auto", 250, 2300)])

    # ACT
    load = EnumerationSolutionProvider().solve(ready_to_solve(flight))

    # ASSERT
    assert loaded_ids(load) == ["S1", "S2"]
    assert load.total_revenue_usd == 5300


def test_the_load_with_the_highest_revenue_is_chosen():
    # ARRANGE — only one of the two fits; S2 earns more
    flight = a_flight(300, [("S1", "Atlas Steel", 300, 3000), ("S2", "Bighorn Auto", 250, 3500)])

    # ACT
    load = EnumerationSolutionProvider().solve(ready_to_solve(flight))

    # ASSERT
    assert loaded_ids(load) == ["S2"]


def test_two_lighter_shipments_can_beat_the_single_most_valuable_one():
    # ARRANGE — S1 is the most valuable shipment, but S2 + S3 fit together
    # and earn 2000 + 1800 = 3800, more than S1's 3000.
    flight = a_flight(
        500,
        [("S1", "Atlas Steel", 500, 3000), ("S2", "Bighorn Auto", 250, 2000), ("S3", "Cedar Pharma", 250, 1800)],
    )

    # ACT
    load = EnumerationSolutionProvider().solve(ready_to_solve(flight))

    # ASSERT
    assert loaded_ids(load) == ["S2", "S3"]
    assert load.total_revenue_usd == 3800


def test_the_load_never_exceeds_the_weight_limit():
    # ARRANGE — all three together would weigh 900 kg on a 600 kg flight
    flight = a_flight(
        600,
        [("S1", "Atlas Steel", 300, 3000), ("S2", "Bighorn Auto", 300, 2900), ("S3", "Cedar Pharma", 300, 2800)],
    )

    # ACT
    load = EnumerationSolutionProvider().solve(ready_to_solve(flight))

    # ASSERT
    assert load.total_weight_kg <= 600
    assert load.total_revenue_usd == 5900
