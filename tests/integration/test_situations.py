"""End-to-end tests: the real command line, the real solver, prepared flights.

Each test runs `python -m cli optimize_cargo <flight>` the way the planner
would (through cli.main(), in this same process so it stays fast) against a
named situation under tests/resources/, and checks only what the planner can
observe: what is printed and how the program ends.

Where several loads share the highest revenue, only the revenue is checked:
which of those loads is returned is deliberately left to the solver.
"""

from pathlib import Path

import pytest

import cli

_RESOURCES_DIR = Path(__file__).parent.parent / "resources"
_DATA_DIR = Path(__file__).parent.parent.parent / "data"


def _run_cli(
    flight_id: str,
    data_folder: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> tuple[str, int]:
    """Run cli.main() for one flight.

    Args:
        flight_id: Name of the subfolder under data_folder holding the flight.
        data_folder: Folder passed as --data-folder.
        monkeypatch: Used to substitute sys.argv for the duration of the call.
        capsys: Used to capture what the program prints.

    Returns:
        Everything the program printed, and its exit code.
    """
    monkeypatch.setattr("sys.argv", ["cli", "optimize_cargo", flight_id, "--data-folder", str(data_folder)])
    with pytest.raises(SystemExit) as exc_info:
        cli.main()
    return capsys.readouterr().out, exc_info.value.code


def _decisions(printed: str) -> dict[str, str]:
    """Read the table back as {shipment id: decision}."""
    lines = printed.splitlines()
    # The rule of dashes under the header shows where each column starts.
    rule_index = next(i for i, line in enumerate(lines) if line.startswith("---"))
    decision_start = lines[rule_index].rindex(" ") + 1
    decisions = {}
    for line in lines[rule_index + 1 :]:
        if not line:
            break
        decisions[line.split()[0]] = line[decision_start:]
    return decisions


def _total(printed: str, label: str) -> str:
    """Return the text after a totals label such as "Revenue"."""
    line = next(line for line in printed.splitlines() if line.startswith(label))
    return line[len(label) :].strip()


@pytest.mark.integration
def test_the_load_with_the_highest_revenue_is_recommended(monkeypatch, capsys):
    # ARRANGE / ACT — S2 + S3 fit together and earn $3,800, more than S1's $3,000
    printed, exit_code = _run_cli("unique_optimum", _RESOURCES_DIR, monkeypatch, capsys)

    # ASSERT
    assert exit_code == 0
    assert _decisions(printed) == {"S1": "left behind", "S2": "LOADED", "S3": "LOADED"}
    assert _total(printed, "Revenue") == "$3,800"


@pytest.mark.integration
def test_the_recommended_load_never_exceeds_the_weight_limit(monkeypatch, capsys):
    # ARRANGE / ACT — three 300 kg shipments on a 600 kg flight: only two can fly
    printed, exit_code = _run_cli("weight_limit_binding", _RESOURCES_DIR, monkeypatch, capsys)

    # ASSERT — the two most valuable fly; the third stays even though it would add revenue
    assert exit_code == 0
    assert _decisions(printed) == {"S1": "LOADED", "S2": "LOADED", "S3": "left behind"}
    assert _total(printed, "Weight used") == "600 of 600 kg"
    assert _total(printed, "Revenue") == "$5,900"


@pytest.mark.integration
def test_a_shipment_too_heavy_for_the_aircraft_is_left_behind_and_the_rest_is_planned(monkeypatch, capsys):
    # ARRANGE / ACT — S2 weighs 900 kg on a 500 kg flight, however much it would earn
    printed, exit_code = _run_cli("oversize_shipment_left_behind", _RESOURCES_DIR, monkeypatch, capsys)

    # ASSERT
    assert exit_code == 0
    assert _decisions(printed) == {
        "S1": "LOADED",
        "S2": "left behind (over weight limit)",
        "S3": "left behind",
    }
    assert _total(printed, "Revenue") == "$3,000"


@pytest.mark.integration
def test_when_no_shipment_fits_the_planner_is_told_so(monkeypatch, capsys):
    # ARRANGE / ACT — every shipment alone weighs more than the aircraft can carry
    printed, exit_code = _run_cli("no_shipment_fits", _RESOURCES_DIR, monkeypatch, capsys)

    # ASSERT
    assert exit_code == 1
    assert "No shipment fits on this flight" in printed
    assert "LOADED" not in printed


@pytest.mark.integration
def test_when_several_loads_earn_the_same_the_best_revenue_is_still_reached(monkeypatch, capsys):
    # ARRANGE / ACT — S1 and S2 are interchangeable and only one of them fits
    printed, exit_code = _run_cli("multiple_optimal_loads", _RESOURCES_DIR, monkeypatch, capsys)

    # ASSERT — the shared best revenue, never which of the two was chosen
    assert exit_code == 0
    assert _total(printed, "Revenue") == "$1,000"
    assert sorted(_decisions(printed).values()) == ["LOADED", "left behind"]


@pytest.mark.integration
@pytest.mark.parametrize(
    "situation, reason",
    [
        ("invalid_negative_weight", "shipment 'S2' has weight -250 kg; weight must be greater than 0"),
        ("invalid_missing_weight_limit", "the flight is missing 'maxWeightKg'"),
        ("invalid_not_json", "is not valid JSON (line 4)"),
        ("a_flight_that_does_not_exist", "no data was found for flight 'a_flight_that_does_not_exist'"),
    ],
)
def test_wrong_or_missing_data_is_explained_instead_of_planned(monkeypatch, capsys, situation, reason):
    # ARRANGE / ACT
    printed, exit_code = _run_cli(situation, _RESOURCES_DIR, monkeypatch, capsys)

    # ASSERT — one sentence for the planner: no table, and no Python traceback
    assert exit_code == 2
    assert printed.startswith("Cannot plan this flight: ")
    assert reason in printed
    assert len(printed.splitlines()) == 1


@pytest.mark.integration
def test_the_workshop_flight_loads_the_four_shipments_that_earn_the_most(monkeypatch, capsys):
    # ARRANGE / ACT — the flight shown at the workshop, read from the real data/ folder
    printed, exit_code = _run_cli("SC101", _DATA_DIR, monkeypatch, capsys)

    # ASSERT — this flight has exactly one highest-revenue load, so the load itself can be checked
    assert exit_code == 0
    decisions = _decisions(printed)
    assert [shipment for shipment, decision in decisions.items() if decision == "LOADED"] == ["S1", "S2", "S3", "S4"]
    assert _total(printed, "Shipments") == "4 loaded, 5 left behind"
    assert _total(printed, "Revenue") == "$9,600"
    assert _total(printed, "Weight used") == "1,000 of 1,000 kg"


@pytest.mark.integration
def test_the_small_example_flight_can_be_checked_by_hand(monkeypatch, capsys):
    # ARRANGE / ACT — the three-shipment flight in the real data/ folder
    printed, exit_code = _run_cli("SC001", _DATA_DIR, monkeypatch, capsys)

    # ASSERT
    assert exit_code == 0
    assert _decisions(printed) == {"S1": "left behind", "S2": "LOADED", "S3": "LOADED"}
    assert _total(printed, "Revenue") == "$3,800"
