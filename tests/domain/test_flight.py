import pytest

from domain.flight import Flight
from domain.shipment import Shipment


@pytest.fixture
def steel() -> Shipment:
    return Shipment(id="S1", customer="Atlas Steel", weight_kg=300, revenue_usd=3000)


def test_a_flight_keeps_its_weight_limit_and_shipments(steel):
    # ARRANGE / ACT
    flight = Flight(flight_id="SC101", max_weight_kg=1000, shipments=[steel])

    # ASSERT
    assert flight.flight_id == "SC101"
    assert flight.max_weight_kg == 1000
    assert flight.shipments == [steel]


def test_a_flight_without_an_id_is_rejected(steel):
    with pytest.raises(ValueError, match="needs an id"):
        Flight(flight_id="", max_weight_kg=1000, shipments=[steel])


@pytest.mark.parametrize("max_weight_kg", [0, -1000])
def test_a_flight_with_no_weight_limit_or_a_negative_one_is_rejected(steel, max_weight_kg):
    with pytest.raises(ValueError, match="weight limit .* must be greater than 0"):
        Flight(flight_id="SC101", max_weight_kg=max_weight_kg, shipments=[steel])


def test_a_flight_with_no_shipments_is_rejected():
    with pytest.raises(ValueError, match="no shipments"):
        Flight(flight_id="SC101", max_weight_kg=1000, shipments=[])


def test_a_flight_with_two_shipments_sharing_an_id_is_rejected(steel):
    # ARRANGE — a different shipment that reuses the id "S1"
    same_id = Shipment(id="S1", customer="Bighorn Auto", weight_kg=100, revenue_usd=500)

    # ACT / ASSERT
    with pytest.raises(ValueError, match="'S1' appears more than once"):
        Flight(flight_id="SC101", max_weight_kg=1000, shipments=[steel, same_id])


def test_a_flight_may_carry_several_shipments_for_the_same_customer(steel):
    # ARRANGE — a second shipment for Atlas Steel, with its own id
    more_steel = Shipment(id="S2", customer="Atlas Steel", weight_kg=250, revenue_usd=2400)

    # ACT
    flight = Flight(flight_id="SC101", max_weight_kg=1000, shipments=[steel, more_steel])

    # ASSERT
    assert len(flight.shipments) == 2
