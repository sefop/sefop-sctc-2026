"""
ROLE: Abstract Base Class — contract that every data-loading strategy must follow.

WHY THIS EXISTS:
    The use case loads a flight through this interface, so the source of data
    (JSON file, spreadsheet, database, the airline's booking system, etc.) can
    change without modifying the optimization logic itself.

WHERE IMPLEMENTATIONS LIVE:
    Concrete loaders live in src/adapters/, e.g. json_data_loader.py.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from domain.flight import Flight


class BaseDataLoader(ABC):
    """
    An abstract base class (ABC) is like a contract: it declares methods
    that every data loader **must** implement, without dictating *how* the
    data is fetched. Any class that inherits from ``BaseDataLoader`` must
    provide a ``load()`` method, so the rest of the system can load a flight
    without caring whether it comes from a file, a database, or an API.
    """

    @abstractmethod
    def load(self, flight_id: str) -> Flight | None:
        """Load the flight with the given id.

        Args:
            flight_id: Identifier of the flight to load.

        Returns:
            The loaded Flight, or None if no data exists for that id.

        Raises:
            ValueError: If data exists but is malformed or describes an
                impossible flight. The message says what to correct.
        """
