from tests.builders import a_flight, loaded_ids, ready_to_solve
from use_cases.solving.optimization.mip_highs.mip_highs_solution_provider import MipHighsSolutionProvider


def test_everything_flies_when_everything_fits():
    # ARRANGE — 300 + 250 = 550 kg on a 1000 kg flight
    flight = a_flight(1000, [("S1", "Atlas Steel", 300, 3000), ("S2", "Bighorn Auto", 250, 2300)])

    # ACT
    load = MipHighsSolutionProvider().solve(ready_to_solve(flight))

    # ASSERT
    assert sorted(loaded_ids(load)) == ["S1", "S2"]
    assert load.total_revenue_usd == 5300


def test_two_lighter_shipments_can_beat_the_single_most_valuable_one():
    # ARRANGE — S2 + S3 fit together and earn 3800, more than S1's 3000
    flight = a_flight(
        500,
        [("S1", "Atlas Steel", 500, 3000), ("S2", "Bighorn Auto", 250, 2000), ("S3", "Cedar Pharma", 250, 1800)],
    )

    # ACT
    load = MipHighsSolutionProvider().solve(ready_to_solve(flight))

    # ASSERT
    assert sorted(loaded_ids(load)) == ["S2", "S3"]
    assert load.total_revenue_usd == 3800


def test_a_shipment_is_loaded_whole_or_not_at_all():
    # ARRANGE — loading two thirds of S1 would fill the aircraft and earn 2000,
    # but a shipment cannot be split, so the best real load is S2 alone.
    flight = a_flight(200, [("S1", "Atlas Steel", 300, 3000), ("S2", "Bighorn Auto", 200, 1000)])

    # ACT
    load = MipHighsSolutionProvider().solve(ready_to_solve(flight))

    # ASSERT
    assert loaded_ids(load) == ["S2"]
    assert load.total_revenue_usd == 1000


def test_the_load_never_exceeds_the_weight_limit():
    # ARRANGE — all three together would weigh 900 kg on a 600 kg flight
    flight = a_flight(
        600,
        [("S1", "Atlas Steel", 300, 3000), ("S2", "Bighorn Auto", 300, 2900), ("S3", "Cedar Pharma", 300, 2800)],
    )

    # ACT
    load = MipHighsSolutionProvider().solve(ready_to_solve(flight))

    # ASSERT
    assert load.total_weight_kg <= 600
    assert load.total_revenue_usd == 5900


def test_the_solver_prints_nothing_on_the_planners_console(capfd):
    # ARRANGE
    flight = a_flight(1000, [("S1", "Atlas Steel", 300, 3000)])

    # ACT
    MipHighsSolutionProvider().solve(ready_to_solve(flight))

    # ASSERT — capfd also captures output written by the solver's own C++ code
    assert capfd.readouterr().out == ""


def test_decision_variables_are_named_after_their_shipment():
    assert MipHighsSolutionProvider.variable_name("S1") == "load_S1"
