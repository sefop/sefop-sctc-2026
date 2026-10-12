from __future__ import annotations

from domain.flight import Flight
from tests.builders import a_flight, loaded_ids
from use_cases.optimization_response import Outcome
from use_cases.ports.base_data_loader import BaseDataLoader
from use_cases.solving.optimization.enumeration.enumeration_solution_provider import EnumerationSolutionProvider
from use_cases.solving.orchestrator import Orchestrator
from use_cases.solving.postprocessing.postprocessing import PostProcess
from use_cases.solving.preprocessing.preprocessing import PreProcess
from use_cases.use_case_optimize_cargo import OptimizeCargo


class _InMemoryLoader(BaseDataLoader):
    """Fake loader: serves flights from a dict, or raises a prepared error."""

    def __init__(self, flights: dict[str, Flight] | None = None, error: ValueError | None = None) -> None:
        self._flights = flights or {}
        self._error = error

    def load(self, flight_id: str) -> Flight | None:
        if self._error is not None:
            raise self._error
        return self._flights.get(flight_id)


def _optimize_cargo(loader: BaseDataLoader) -> OptimizeCargo:
    # The brute-force provider keeps these tests about the use case's own
    # behavior, independent of any solver library.
    orchestrator = Orchestrator(
        preprocessing=PreProcess(),
        postprocessing=PostProcess(),
        solution_provider=EnumerationSolutionProvider(),
    )
    return OptimizeCargo(flight_loader=loader, orchestrator=orchestrator)


def test_a_valid_flight_gets_the_load_with_the_highest_revenue():
    # ARRANGE — S2 + S3 fit together and earn 3800, more than S1's 3000
    flight = a_flight(
        500,
        [("S1", "Atlas Steel", 500, 3000), ("S2", "Bighorn Auto", 250, 2000), ("S3", "Cedar Pharma", 250, 1800)],
    )
    loader = _InMemoryLoader({"SC001": flight})

    # ACT
    response = _optimize_cargo(loader).optimize("SC001")

    # ASSERT
    assert response.outcome is Outcome.LOADED
    assert response.load is not None
    assert loaded_ids(response.load) == ["S2", "S3"]
    assert response.load.total_revenue_usd == 3800


def test_a_flight_where_every_shipment_is_too_heavy_reports_that_no_shipment_fits():
    # ARRANGE
    flight = a_flight(100, [("S1", "Atlas Steel", 300, 3000), ("S2", "Bighorn Auto", 250, 2300)])
    loader = _InMemoryLoader({"SC002": flight})

    # ACT
    response = _optimize_cargo(loader).optimize("SC002")

    # ASSERT
    assert response.outcome is Outcome.NO_SHIPMENT_FITS
    assert response.flight is flight
    assert response.load is None


def test_an_unknown_flight_is_reported_as_invalid_input():
    # ARRANGE
    loader = _InMemoryLoader({})

    # ACT
    response = _optimize_cargo(loader).optimize("SC999")

    # ASSERT
    assert response.outcome is Outcome.INVALID_INPUT
    assert response.message == "no data was found for flight 'SC999'"


def test_wrong_flight_data_is_reported_as_invalid_input_with_the_reason():
    # ARRANGE
    loader = _InMemoryLoader(error=ValueError("shipment 'S2' has weight -250 kg; weight must be greater than 0"))

    # ACT
    response = _optimize_cargo(loader).optimize("SC101")

    # ASSERT
    assert response.outcome is Outcome.INVALID_INPUT
    assert response.message == "shipment 'S2' has weight -250 kg; weight must be greater than 0"
