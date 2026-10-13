"""
ROLE: Unit tests for what cli.main() itself decides.

WHY THIS EXISTS:
    tests/integration/test_situations.py exercises cli.main() end-to-end, but
    every one of those runs passes an explicit --data-folder. This file covers
    what is left: falling back to Settings().folder_path, which is a relative
    path ("data") resolved against the current working directory, and the
    command-line surface itself.
"""

import json

import pytest

import cli


def _write_flight(data_root, flight_id: str, payload: dict) -> None:
    folder = data_root / flight_id
    folder.mkdir(parents=True)
    (folder / "data.json").write_text(json.dumps(payload), encoding="utf-8")


def test_without_a_data_folder_flights_are_read_from_the_data_folder_next_to_where_it_runs(
    tmp_path, monkeypatch, capsys
):
    # ARRANGE — Settings().folder_path is relative ("data"), so chdir into a temp
    # directory to prove main() finds it from the current working directory.
    monkeypatch.chdir(tmp_path)
    _write_flight(
        tmp_path / "data",
        "SC001",
        {
            "flightId": "SC001",
            "maxWeightKg": 500,
            "shipments": [{"id": "S1", "customer": "Atlas Steel", "weightKg": 300, "revenueUsd": 3000}],
        },
    )
    monkeypatch.setattr("sys.argv", ["cli", "optimize_cargo", "SC001"])

    # ACT
    with pytest.raises(SystemExit) as exc_info:
        cli.main()

    # ASSERT
    assert exc_info.value.code == 0
    assert "Flight SC001" in capsys.readouterr().out


def test_a_command_is_required(monkeypatch, capsys):
    # ARRANGE
    monkeypatch.setattr("sys.argv", ["cli"])

    # ACT
    with pytest.raises(SystemExit) as exc_info:
        cli.main()

    # ASSERT — argparse's own "you mistyped the command" exit code
    assert exc_info.value.code == 2
    assert "optimize_cargo" in capsys.readouterr().err


def test_a_flight_that_cannot_be_read_goes_straight_from_reading_to_the_result(tmp_path, monkeypatch, capfd):
    # ARRANGE
    monkeypatch.setattr("sys.argv", ["cli", "optimize_cargo", "SC999", "--data-folder", str(tmp_path)])

    # ACT
    with pytest.raises(SystemExit):
        cli.main()

    # ASSERT — the whole screen, and nothing on the error stream
    captured = capfd.readouterr()
    assert captured.out == (
        "\n"
        "#----------------------------------#\n"
        "#            Read data             #\n"
        "#----------------------------------#\n"
        "\n"
        "#----------------------------------#\n"
        "#              Result              #\n"
        "#----------------------------------#\n"
        "Cannot plan this flight: no data was found for flight 'SC999'.\n"
    )
    assert captured.err == ""


def test_the_solver_log_is_off_unless_asked_for(tmp_path, monkeypatch, capfd):
    # ARRANGE
    _write_flight(
        tmp_path,
        "SC001",
        {
            "flightId": "SC001",
            "maxWeightKg": 500,
            "shipments": [{"id": "S1", "customer": "Atlas Steel", "weightKg": 300, "revenueUsd": 3000}],
        },
    )
    monkeypatch.setattr("sys.argv", ["cli", "optimize_cargo", "SC001", "--data-folder", str(tmp_path)])

    # ACT
    with pytest.raises(SystemExit):
        cli.main()

    # ASSERT — the Solve stage shows the solver's name and status, not its log
    printed = capfd.readouterr().out
    assert "Solver: MIP (HiGHS)\nStatus: Optimal\n" in printed
    assert "Running HiGHS" not in printed


def test_verbose_shows_the_solver_log_inside_the_solve_stage(tmp_path, monkeypatch, capfd):
    # ARRANGE
    _write_flight(
        tmp_path,
        "SC001",
        {
            "flightId": "SC001",
            "maxWeightKg": 500,
            "shipments": [{"id": "S1", "customer": "Atlas Steel", "weightKg": 300, "revenueUsd": 3000}],
        },
    )
    monkeypatch.setattr("sys.argv", ["cli", "--verbose", "optimize_cargo", "SC001", "--data-folder", str(tmp_path)])

    # ACT
    with pytest.raises(SystemExit) as exc_info:
        cli.main()

    # ASSERT — capfd also captures output written by the solver's own C++ code
    printed = capfd.readouterr().out
    assert exc_info.value.code == 0
    assert "Flight SC001" in printed
    solver_log = printed.index("Running HiGHS")
    assert printed.index("Solver: MIP (HiGHS)") < solver_log < printed.index("Status: Optimal")
