import pytest

from domain.flight import Flight
from domain.load import Load
from domain.shipment import Shipment


@pytest.fixture
def steel() -> Shipment:
    return Shipment(id="S1", customer="Atlas Steel", weight_kg=300, revenue_usd=3000)


@pytest.fixture
def auto_parts() -> Shipment:
    return Shipment(id="S2", customer="Bighorn Auto", weight_kg=250, revenue_usd=2300)


@pytest.fixture
def medicine() -> Shipment:
    return Shipment(id="S3", customer="Cedar Pharma", weight_kg=100, revenue_usd=800)


@pytest.fixture
def flight(steel, auto_parts, medicine) -> Flight:
    return Flight(flight_id="SC101", max_weight_kg=600, shipments=[steel, auto_parts, medicine])


def test_a_load_adds_up_the_revenue_and_weight_of_what_flies(flight, steel, auto_parts):
    # ARRANGE / ACT
    load = Load(flight=flight, loaded=[steel, auto_parts])

    # ASSERT
    assert load.total_revenue_usd == 3000 + 2300
    assert load.total_weight_kg == 300 + 250


def test_a_load_lists_every_other_shipment_as_left_behind(flight, steel, auto_parts, medicine):
    # ARRANGE / ACT
    load = Load(flight=flight, loaded=[auto_parts])

    # ASSERT — in the flight's own order
    assert load.left_behind == [steel, medicine]


def test_a_load_may_use_the_weight_limit_exactly(flight, steel, auto_parts):
    # ARRANGE — a second flight whose limit equals the two shipments' weight
    exact = Flight(flight_id="SC102", max_weight_kg=550, shipments=flight.shipments)

    # ACT
    load = Load(flight=exact, loaded=[steel, auto_parts])

    # ASSERT
    assert load.total_weight_kg == exact.max_weight_kg


def test_a_load_never_exceeds_the_weight_limit(flight, steel, auto_parts, medicine):
    # ACT / ASSERT — 300 + 250 + 100 = 650 kg on a 600 kg flight
    with pytest.raises(ValueError, match="exceeds the weight limit"):
        Load(flight=flight, loaded=[steel, auto_parts, medicine])


def test_a_load_with_nothing_on_board_is_valid(flight):
    # ARRANGE / ACT
    load = Load(flight=flight, loaded=[])

    # ASSERT
    assert load.total_revenue_usd == 0
    assert load.total_weight_kg == 0
    assert load.left_behind == flight.shipments


def test_a_load_cannot_carry_a_shipment_from_another_flight(flight):
    # ARRANGE — a shipment that was never on this flight
    stranger = Shipment(id="X9", customer="Elk Outfitters", weight_kg=10, revenue_usd=100)

    # ACT / ASSERT
    with pytest.raises(ValueError, match="'X9' is not on flight 'SC101'"):
        Load(flight=flight, loaded=[stranger])


def test_a_load_cannot_carry_the_same_shipment_twice(flight, medicine):
    with pytest.raises(ValueError, match="'S3' is loaded more than once"):
        Load(flight=flight, loaded=[medicine, medicine])
