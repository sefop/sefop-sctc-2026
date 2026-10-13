"""
ROLE: Entry point — the command line the planner types into.

WHY THIS EXISTS:
    Something has to turn typed words into a call to the program and turn the
    outcome back into something the terminal understands (text and an exit
    code). That is all this file does: it reads the arguments, switches the
    stage log on, and hands over to whatever startup.py assembles. It never
    builds a concrete adapter or use case itself, so replacing the terminal
    with another front end (a web page, a scheduled job) means writing a new
    entry point next to this one, not changing the program behind it.

HOW TO RUN:
    python -m cli optimize_cargo <flight_id>
    python -m cli --verbose optimize_cargo <flight_id>
"""

from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import replace

import startup
from startup import Settings
from use_cases.optimization_response import Outcome
from use_cases.stage_log import log_stage

logger = logging.getLogger(__name__)

# What the program tells the operating system when it ends, one code per
# outcome, so a script calling this program can tell the outcomes apart
# without reading the printed text. 0 conventionally means "all went well";
# 2 is also what argparse itself uses for a mistyped command.
_EXIT_CODES = {
    Outcome.LOADED: 0,
    Outcome.NO_SHIPMENT_FITS: 1,
    Outcome.INVALID_INPUT: 2,
}


def _build_parser() -> argparse.ArgumentParser:
    """Build the argparse parser with its one subcommand: optimize_cargo."""
    parser = argparse.ArgumentParser(description="Decision support for an airline cargo load planner")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Also show the solver's own log inside the Solve stage (off by default to keep the output short).",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    optimize_parser = subparsers.add_parser(
        "optimize_cargo",
        help="Choose the shipments that fly: highest revenue within the aircraft's weight limit",
    )
    optimize_parser.add_argument(
        "flight_id", help="Flight to plan (must match a subfolder under the data/ directory, e.g. SC101)."
    )
    optimize_parser.add_argument(
        "--data-folder",
        default=None,
        help="Override the folder containing flight subfolders (default: Settings().folder_path).",
    )

    return parser


def _optimize_cargo(args: argparse.Namespace, settings: Settings) -> int:
    """Plan one flight and print the outcome.

    Args:
        args: The parsed command line; flight_id and data_folder are read.
        settings: The default settings, before the command line overrides them.

    Returns:
        The process exit code for the outcome, as listed in _EXIT_CODES.
    """
    data_folder = args.data_folder or settings.folder_path
    # Settings is copied with the new folder rather than modified, so the
    # defaults stay untouched for anything else that reads them.
    settings = replace(settings, folder_path=data_folder)

    optimize_cargo = startup.build_optimize_cargo(settings)
    writer = startup.build_result_writer()

    response = optimize_cargo.optimize(args.flight_id)
    # The Result stage is announced here, not in the use case, because
    # presenting the outcome is this entry point's job: the use case returns a
    # response and does not know it will be printed.
    log_stage(logger, "Result")
    writer.write(response)

    return _EXIT_CODES[response.outcome]


def main() -> None:
    """Run the command typed by the planner and end the process with its exit code."""
    parser = _build_parser()
    args = parser.parse_args()
    settings = Settings(show_solver_log=args.verbose)

    # The stages of a run are announced through Python's logging. They go to
    # standard output, as plain text, so the stage boxes, the solver's log and
    # the result table appear on screen in the order they happen.
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
    try:
        if args.command == "optimize_cargo":
            exit_code = _optimize_cargo(args, settings)
        else:
            raise AssertionError(f"Unhandled command: {args.command}")
    finally:
        # Removed even when the run fails, so calling main() twice in one
        # process (as the tests do) never prints every line twice.
        root_logger.removeHandler(handler)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
