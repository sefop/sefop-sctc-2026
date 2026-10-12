from domain.load import Load
from tests.builders import a_flight
from use_cases.optimization_response import OptimizationResponse, Outcome


def test_a_loaded_response_carries_the_load_and_its_flight():
    # ARRANGE
    flight = a_flight(1000, [("S1", "Atlas Steel", 300, 3000)])
    load = Load(flight=flight, loaded=list(flight.shipments))

    # ACT
    response = OptimizationResponse.loaded(load)

    # ASSERT
    assert response.outcome is Outcome.LOADED
    assert response.load is load
    assert response.flight is flight
    assert response.message is None


def test_a_no_shipment_fits_response_carries_the_flight_but_no_load():
    # ARRANGE
    flight = a_flight(100, [("S1", "Atlas Steel", 300, 3000)])

    # ACT
    response = OptimizationResponse.no_shipment_fits(flight)

    # ASSERT
    assert response.outcome is Outcome.NO_SHIPMENT_FITS
    assert response.flight is flight
    assert response.load is None


def test_an_invalid_input_response_carries_only_the_explanation():
    # ACT
    response = OptimizationResponse.invalid_input("the flight is missing 'maxWeightKg'")

    # ASSERT
    assert response.outcome is Outcome.INVALID_INPUT
    assert response.message == "the flight is missing 'maxWeightKg'"
    assert response.flight is None
    assert response.load is None
