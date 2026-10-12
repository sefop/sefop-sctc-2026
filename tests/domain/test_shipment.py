import pytest

from domain.shipment import Shipment


def test_a_shipment_keeps_its_customer_weight_and_revenue():
    # ARRANGE / ACT
    shipment = Shipment(id="S1", customer="Atlas Steel", weight_kg=300, revenue_usd=3000)

    # ASSERT
    assert shipment.id == "S1"
    assert shipment.customer == "Atlas Steel"
    assert shipment.weight_kg == 300
    assert shipment.revenue_usd == 3000


def test_a_shipment_cannot_be_changed_after_it_is_created():
    # ARRANGE
    shipment = Shipment(id="S1", customer="Atlas Steel", weight_kg=300, revenue_usd=3000)

    # ACT / ASSERT
    with pytest.raises(AttributeError):
        shipment.weight_kg = 1  # type: ignore[misc]


def test_a_shipment_without_an_id_is_rejected():
    with pytest.raises(ValueError, match="needs an id"):
        Shipment(id="", customer="Atlas Steel", weight_kg=300, revenue_usd=3000)


def test_a_shipment_without_a_customer_is_rejected():
    with pytest.raises(ValueError, match="'S1' has no customer"):
        Shipment(id="S1", customer="", weight_kg=300, revenue_usd=3000)


@pytest.mark.parametrize("weight_kg", [0, -5])
def test_a_shipment_with_no_weight_or_negative_weight_is_rejected(weight_kg):
    with pytest.raises(ValueError, match="'S1' has weight .* must be greater than 0"):
        Shipment(id="S1", customer="Atlas Steel", weight_kg=weight_kg, revenue_usd=3000)


@pytest.mark.parametrize("revenue_usd", [0, -100])
def test_a_shipment_with_no_revenue_or_negative_revenue_is_rejected(revenue_usd):
    with pytest.raises(ValueError, match="'S1' has revenue .* must be greater than 0"):
        Shipment(id="S1", customer="Atlas Steel", weight_kg=300, revenue_usd=revenue_usd)
