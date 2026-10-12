from __future__ import annotations

from domain.load import Load
from tests.builders import a_flight, loaded_ids
from use_cases.solving.optimization.solution_provider import SolutionProvider
from use_cases.solving.orchestrator import Orchestrator
from use_cases.solving.postprocessing.postprocessing import PostProcess
from use_cases.solving.preprocessing.pre_processed_data import PreProcessedData
from use_cases.solving.preprocessing.preprocessing import PreProcess


class _LoadsEverythingItIsGiven(SolutionProvider):
    """Fake provider: loads every shipment it receives, in reverse order, and records the call."""

    def __init__(self) -> None:
        self.received: PreProcessedData | None = None

    @property
    def name(self) -> str:
        return "Fake"

    def solve(self, data: PreProcessedData) -> Load | None:
        self.received = data
        return Load(flight=data.flight, loaded=list(reversed(data.feasible_shipments)))


class _FindsNothing(SolutionProvider):
    """Fake provider that fails to produce a load."""

    @property
    def name(self) -> str:
        return "Fake"

    def solve(self, data: PreProcessedData) -> Load | None:
        return None


def _orchestrator(provider: SolutionProvider) -> Orchestrator:
    return Orchestrator(preprocessing=PreProcess(), postprocessing=PostProcess(), solution_provider=provider)


def test_the_solver_only_sees_shipments_that_fit_on_their_own():
    # ARRANGE — S2 alone is heavier than the aircraft can carry
    flight = a_flight(500, [("S1", "Atlas Steel", 300, 3000), ("S2", "Bighorn Auto", 900, 9000)])
    provider = _LoadsEverythingItIsGiven()

    # ACT
    _orchestrator(provider).solve(flight)

    # ASSERT
    assert provider.received is not None
    assert [s.id for s in provider.received.feasible_shipments] == ["S1"]


def test_the_load_comes_back_in_the_order_of_the_flight():
    # ARRANGE — the fake provider returns shipments in reverse order
    flight = a_flight(1000, [("S1", "Atlas Steel", 300, 3000), ("S2", "Bighorn Auto", 250, 2300)])

    # ACT
    load = _orchestrator(_LoadsEverythingItIsGiven()).solve(flight)

    # ASSERT
    assert load is not None
    assert loaded_ids(load) == ["S1", "S2"]


def test_no_load_is_returned_and_the_solver_is_not_called_when_no_shipment_fits():
    # ARRANGE
    flight = a_flight(100, [("S1", "Atlas Steel", 300, 3000), ("S2", "Bighorn Auto", 250, 2300)])
    provider = _LoadsEverythingItIsGiven()

    # ACT
    load = _orchestrator(provider).solve(flight)

    # ASSERT
    assert load is None
    assert provider.received is None


def test_no_load_is_returned_when_the_solver_finds_none():
    # ARRANGE
    flight = a_flight(1000, [("S1", "Atlas Steel", 300, 3000)])

    # ACT
    load = _orchestrator(_FindsNothing()).solve(flight)

    # ASSERT
    assert load is None
