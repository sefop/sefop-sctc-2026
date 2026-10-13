"""
ROLE: Implementation of BaseResultWriter that prints the outcome to the terminal.

WHY THIS EXISTS:
    This module is the only place in the codebase that decides how an outcome
    looks to the planner. It prints one short table per run, in plain text, so
    it stays readable when projected and works in any terminal. The stage
    boxes printed above the table are not drawn here: they come from the log
    (use_cases/stage_log.py). A different
    presentation (a file, a web page) is a new BaseResultWriter, not a change
    here.
"""

from __future__ import annotations

import sys
from typing import TextIO

from domain.flight import Flight
from domain.load import Load
from domain.shipment import Shipment
from use_cases.optimization_response import OptimizationResponse, Outcome
from use_cases.ports.base_result_writer import BaseResultWriter

_LOADED = "LOADED"
_LEFT_BEHIND = "left behind"
_LEFT_BEHIND_OVERSIZE = "left behind (over weight limit)"

# Blank space between two columns of the table.
_COLUMN_GAP = "  "


class ConsoleResultWriter(BaseResultWriter):
    """Prints each outcome as plain text, using only the standard library.

    Each of the three outcomes has its own, distinct presentation, worded for
    the planner rather than for a programmer.
    """

    def __init__(self, stream: TextIO | None = None) -> None:
        # None means "whatever sys.stdout is when write() is called", looked
        # up late so that tools which replace sys.stdout (pytest's output
        # capture, for one) still see what is printed. Tests may also pass
        # their own stream.
        self._stream = stream

    def write(self, response: OptimizationResponse) -> None:
        """Print the response: a table for a load, a sentence otherwise."""
        stream = self._stream if self._stream is not None else sys.stdout
        if response.outcome is Outcome.LOADED and response.load is not None:
            lines = _load_lines(response.load)
        elif response.outcome is Outcome.NO_SHIPMENT_FITS and response.flight is not None:
            lines = _no_shipment_fits_lines(response.flight)
        else:
            lines = [f"Cannot plan this flight: {response.message}."]
        print("\n".join(lines), file=stream)


def _load_lines(load: Load) -> list[str]:
    """Build the normal output: every shipment with its decision, then the totals."""
    flight = load.flight
    loaded_ids = {shipment.id for shipment in load.loaded}

    header = ["Shipment", "Customer", "Weight", "Revenue", "Decision"]
    rows = [
        [
            shipment.id,
            shipment.customer,
            _kg(shipment.weight_kg),
            _usd(shipment.revenue_usd),
            _decision(shipment, loaded_ids, flight),
        ]
        # The flight's own order, so the planner finds each shipment where they listed it.
        for shipment in flight.shipments
    ]

    return [
        _title(flight),
        "",
        *_table(header, rows, right_aligned={2, 3}),
        "",
        f"Shipments      {len(load.loaded)} loaded, {len(load.left_behind)} left behind",
        f"Revenue        {_usd(load.total_revenue_usd)}",
        f"Weight used    {_number(load.total_weight_kg)} of {_kg(flight.max_weight_kg)}",
    ]


def _no_shipment_fits_lines(flight: Flight) -> list[str]:
    """Build the output for a flight on which nothing can fly."""
    return [
        _title(flight),
        "",
        "No shipment fits on this flight: each one weighs more than the weight limit.",
    ]


def _title(flight: Flight) -> str:
    return f"Flight {flight.flight_id}   weight limit {_kg(flight.max_weight_kg)}"


def _decision(shipment: Shipment, loaded_ids: set[str], flight: Flight) -> str:
    """Word the decision for one shipment.

    A shipment heavier than the whole weight limit is called out separately:
    it was not outbid by other cargo, it can never fly on this aircraft, and
    the planner needs to know the difference.
    """
    if shipment.id in loaded_ids:
        return _LOADED
    if shipment.weight_kg > flight.max_weight_kg:
        return _LEFT_BEHIND_OVERSIZE
    return _LEFT_BEHIND


def _table(header: list[str], rows: list[list[str]], right_aligned: set[int]) -> list[str]:
    """Lay out a header, a rule of dashes and the rows in aligned columns.

    Args:
        header: Column titles.
        rows: One list of cell texts per row, same length as header.
        right_aligned: Indexes of the columns holding numbers, which read
            best aligned on the right.

    Returns:
        The table's lines, without trailing spaces.
    """
    widths = [max(len(line[i]) for line in [header, *rows]) for i in range(len(header))]

    def lay_out(cells: list[str]) -> str:
        padded = [
            cell.rjust(width) if i in right_aligned else cell.ljust(width)
            for i, (cell, width) in enumerate(zip(cells, widths))
        ]
        return _COLUMN_GAP.join(padded).rstrip()

    rule = _COLUMN_GAP.join("-" * width for width in widths)
    return [lay_out(header), rule, *(lay_out(row) for row in rows)]


def _number(value: float) -> str:
    """Format a number with thousands separators and no needless decimals: 1,000 or 10.5."""
    return f"{value:,.2f}".rstrip("0").rstrip(".")


def _kg(value: float) -> str:
    return f"{_number(value)} kg"


def _usd(value: float) -> str:
    return f"${_number(value)}"
