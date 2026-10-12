"""
ROLE: Implementation of BaseDataLoader that reads Flight data from JSON.

WHY THIS EXISTS:
    This module is the only place in the codebase that knows about JSON files.
    The rest of the system talks to the abstract ``BaseDataLoader`` base class;
    this is one concrete implementation of it.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from domain.flight import Flight
from domain.shipment import Shipment
from use_cases.ports.base_data_loader import BaseDataLoader


class JsonDataLoader(BaseDataLoader):
    """Reads JSON data files and returns domain objects.

    Design note — why camelCase in JSON, not snake_case:
      JSON files use camelCase (e.g. ``maxWeightKg``, ``revenueUsd``) because
      that is the dominant convention for JSON APIs and external data sources.
      This class explicitly maps every camelCase key to its Python snake_case
      equivalent (e.g. ``maxWeightKg`` → ``max_weight_kg``).

      This mapping is intentional and belongs here. This class is the only place
      that knows about JSON — its job is to translate between the external
      world's conventions and the domain model's conventions. Domain objects
      (``Flight``, ``Shipment``) never know about JSON — they only speak Python.
    """

    def __init__(self, folder_path: str) -> None:
        # Store the root folder so tests can point to a temp directory,
        # and production code can point to "data/".
        self._folder_path = Path(folder_path)

    def load(self, flight_id: str) -> Flight | None:
        """Load a Flight from ``{folder_path}/{flight_id}/data.json``.

        Returns None when the file does not exist — callers interpret None as
        "flight not found". Raises ValueError when the file exists but its
        content is invalid, with a message that says what to correct.
        """
        path = self._folder_path / flight_id / "data.json"
        if not path.exists():
            return None  # "not found" — matches BaseDataLoader contract

        raw = path.read_text(encoding="utf-8")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"the data file {path} is not valid JSON (line {exc.lineno})") from exc

        return _parse_flight(data)


def _parse_flight(data: Any) -> Flight:
    """Map a camelCase JSON object to a ``Flight`` domain object.

    Raises ValueError on any missing or invalid field so the caller gets a
    clear message instead of a confusing KeyError or TypeError.
    """
    if not isinstance(data, dict):
        raise ValueError("the data file must contain one flight: an object with flightId, maxWeightKg and shipments")
    raw_shipments = _required(data, "shipments", "the flight")
    if not isinstance(raw_shipments, list):
        raise ValueError("'shipments' must be a list of shipments")
    return Flight(
        flight_id=_text(data, "flightId", "the flight"),
        max_weight_kg=_number(data, "maxWeightKg", "the flight"),
        # Counting from 1 so "shipment number 3" means the third one in the file.
        shipments=[_parse_shipment(raw, position) for position, raw in enumerate(raw_shipments, start=1)],
    )


def _parse_shipment(data: Any, position: int) -> Shipment:
    """Map a camelCase JSON object to a ``Shipment`` domain object.

    Args:
        data: The JSON value found in the shipments list.
        position: 1-based position of the shipment in the file, used to point
            the planner at the right entry when it has no usable id.
    """
    if not isinstance(data, dict):
        raise ValueError(f"shipment number {position} must be an object with id, customer, weightKg and revenueUsd")
    owner = f"shipment number {position}"
    shipment_id = _text(data, "id", owner)
    # Once the id is known, it is a better way to point at the shipment than its position.
    owner = f"shipment '{shipment_id}'"
    return Shipment(
        id=shipment_id,
        customer=_text(data, "customer", owner),
        weight_kg=_number(data, "weightKg", owner),
        revenue_usd=_number(data, "revenueUsd", owner),
    )


def _required(data: dict[str, Any], key: str, owner: str) -> Any:
    """Return data[key], or explain which field of which thing is missing."""
    if key not in data:
        raise ValueError(f"{owner} is missing '{key}'")
    return data[key]


def _text(data: dict[str, Any], key: str, owner: str) -> str:
    """Return data[key] as text, rejecting any other kind of value."""
    value = _required(data, key, owner)
    if not isinstance(value, str):
        raise ValueError(f"'{key}' of {owner} must be text, but it is {json.dumps(value)}")
    return value


def _number(data: dict[str, Any], key: str, owner: str) -> float:
    """Return data[key] as a number, rejecting any other kind of value.

    A number written in quotes ("300") is text, not a number, and is rejected
    rather than silently converted: a file with one such slip often has others.
    """
    value = _required(data, key, owner)
    # bool is checked explicitly because Python treats True/False as the numbers 1/0.
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"'{key}' of {owner} must be a number, but it is {json.dumps(value)}")
    return value
