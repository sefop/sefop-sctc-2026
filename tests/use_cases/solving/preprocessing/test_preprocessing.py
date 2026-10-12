from tests.builders import a_flight
from use_cases.solving.preprocessing.preprocessing import PreProcess


def test_a_shipment_heavier_than_the_weight_limit_is_set_aside():
    # ARRANGE — S2 alone weighs more than the aircraft can carry
    flight = a_flight(500, [("S1", "Atlas Steel", 300, 3000), ("S2", "Bighorn Auto", 501, 9000)])

    # ACT
    data = PreProcess().run(flight)

    # ASSERT
    assert [s.id for s in data.feasible_shipments] == ["S1"]


def test_a_shipment_weighing_exactly_the_limit_can_still_fly():
    # ARRANGE
    flight = a_flight(500, [("S1", "Atlas Steel", 500, 3000)])

    # ACT
    data = PreProcess().run(flight)

    # ASSERT
    assert [s.id for s in data.feasible_shipments] == ["S1"]


def test_the_original_flight_is_kept_with_every_shipment():
    # ARRANGE
    flight = a_flight(500, [("S1", "Atlas Steel", 300, 3000), ("S2", "Bighorn Auto", 501, 9000)])

    # ACT
    data = PreProcess().run(flight)

    # ASSERT — set-aside shipments still belong to the flight, so they can be reported
    assert data.flight is flight
    assert len(data.flight.shipments) == 2


def test_no_shipment_remains_when_every_one_is_too_heavy():
    # ARRANGE
    flight = a_flight(100, [("S1", "Atlas Steel", 300, 3000), ("S2", "Bighorn Auto", 250, 2300)])

    # ACT
    data = PreProcess().run(flight)

    # ASSERT
    assert data.feasible_shipments == []
