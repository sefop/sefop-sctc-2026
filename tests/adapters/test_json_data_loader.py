import json

import pytest

from adapters.json_data_loader import JsonDataLoader


def _valid_payload() -> dict:
    return {
        "flightId": "SC101",
        "maxWeightKg": 1000,
        "shipments": [
            {"id": "S1", "customer": "Atlas Steel", "weightKg": 300, "revenueUsd": 3000},
            {"id": "S2", "customer": "Bighorn Auto", "weightKg": 250.5, "revenueUsd": 2300.75},
        ],
    }


def _loader_for(tmp_path, payload, flight_id: str = "SC101") -> JsonDataLoader:
    """Write payload as {tmp_path}/{flight_id}/data.json and return a loader over tmp_path."""
    folder = tmp_path / flight_id
    folder.mkdir(parents=True)
    content = payload if isinstance(payload, str) else json.dumps(payload)
    (folder / "data.json").write_text(content, encoding="utf-8")
    return JsonDataLoader(folder_path=str(tmp_path))


def test_a_flight_is_read_with_its_weight_limit_and_shipments(tmp_path):
    # ARRANGE
    loader = _loader_for(tmp_path, _valid_payload())

    # ACT
    flight = loader.load("SC101")

    # ASSERT
    assert flight is not None
    assert flight.flight_id == "SC101"
    assert flight.max_weight_kg == 1000
    assert [s.id for s in flight.shipments] == ["S1", "S2"]


def test_each_shipment_is_read_with_its_customer_weight_and_revenue(tmp_path):
    # ARRANGE
    loader = _loader_for(tmp_path, _valid_payload())

    # ACT
    flight = loader.load("SC101")

    # ASSERT
    assert flight is not None
    second = flight.shipments[1]
    assert second.customer == "Bighorn Auto"
    assert second.weight_kg == 250.5
    assert second.revenue_usd == 2300.75


def test_a_flight_with_no_data_file_is_not_found(tmp_path):
    # ARRANGE
    loader = JsonDataLoader(folder_path=str(tmp_path))

    # ACT / ASSERT
    assert loader.load("SC999") is None


def test_a_file_that_is_not_valid_json_is_rejected_with_the_line_to_look_at(tmp_path):
    # ARRANGE — the file stops in the middle of line 2
    loader = _loader_for(tmp_path, '{ "flightId": "SC101",\n  "maxWeightKg": ')

    # ACT / ASSERT
    with pytest.raises(ValueError, match=r"not valid JSON \(line 2\)"):
        loader.load("SC101")


def test_a_file_that_does_not_describe_one_flight_is_rejected(tmp_path):
    # ARRANGE — a list instead of one flight
    loader = _loader_for(tmp_path, [_valid_payload()])

    # ACT / ASSERT
    with pytest.raises(ValueError, match="must contain one flight"):
        loader.load("SC101")


@pytest.mark.parametrize("field", ["flightId", "maxWeightKg", "shipments"])
def test_a_flight_missing_a_field_is_rejected_naming_the_field(tmp_path, field):
    # ARRANGE
    payload = _valid_payload()
    del payload[field]
    loader = _loader_for(tmp_path, payload)

    # ACT / ASSERT
    with pytest.raises(ValueError, match=f"the flight is missing '{field}'"):
        loader.load("SC101")


@pytest.mark.parametrize("field", ["customer", "weightKg", "revenueUsd"])
def test_a_shipment_missing_a_field_is_rejected_naming_the_shipment_and_the_field(tmp_path, field):
    # ARRANGE
    payload = _valid_payload()
    del payload["shipments"][1][field]
    loader = _loader_for(tmp_path, payload)

    # ACT / ASSERT
    with pytest.raises(ValueError, match=f"shipment 'S2' is missing '{field}'"):
        loader.load("SC101")


def test_a_shipment_without_an_id_is_pointed_at_by_its_position_in_the_file(tmp_path):
    # ARRANGE
    payload = _valid_payload()
    del payload["shipments"][1]["id"]
    loader = _loader_for(tmp_path, payload)

    # ACT / ASSERT
    with pytest.raises(ValueError, match="shipment number 2 is missing 'id'"):
        loader.load("SC101")


@pytest.mark.parametrize("not_a_number", ["300", None, True])
def test_a_weight_that_is_not_a_number_is_rejected(tmp_path, not_a_number):
    # ARRANGE — "300" in quotes is text, not a number
    payload = _valid_payload()
    payload["shipments"][0]["weightKg"] = not_a_number
    loader = _loader_for(tmp_path, payload)

    # ACT / ASSERT
    with pytest.raises(ValueError, match="'weightKg' of shipment 'S1' must be a number"):
        loader.load("SC101")


def test_a_weight_limit_that_is_not_a_number_is_rejected(tmp_path):
    # ARRANGE
    payload = _valid_payload()
    payload["maxWeightKg"] = "one thousand"
    loader = _loader_for(tmp_path, payload)

    # ACT / ASSERT
    with pytest.raises(ValueError, match="'maxWeightKg' of the flight must be a number"):
        loader.load("SC101")


def test_shipments_that_are_not_a_list_are_rejected(tmp_path):
    # ARRANGE
    payload = _valid_payload()
    payload["shipments"] = {"S1": "Atlas Steel"}
    loader = _loader_for(tmp_path, payload)

    # ACT / ASSERT
    with pytest.raises(ValueError, match="'shipments' must be a list"):
        loader.load("SC101")


def test_a_negative_weight_is_rejected_naming_the_shipment(tmp_path):
    # ARRANGE — the file is well-formed, but describes an impossible shipment
    payload = _valid_payload()
    payload["shipments"][1]["weightKg"] = -250
    loader = _loader_for(tmp_path, payload)

    # ACT / ASSERT
    with pytest.raises(ValueError, match="shipment 'S2' has weight -250 kg"):
        loader.load("SC101")


def test_two_shipments_sharing_an_id_are_rejected(tmp_path):
    # ARRANGE
    payload = _valid_payload()
    payload["shipments"][1]["id"] = "S1"
    loader = _loader_for(tmp_path, payload)

    # ACT / ASSERT
    with pytest.raises(ValueError, match="'S1' appears more than once"):
        loader.load("SC101")
