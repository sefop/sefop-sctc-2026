"""
ROLE: Abstract Base Class — contract for presenting the outcome of planning a flight.

WHY THIS EXISTS:
    The program has to show every outcome to the planner, but the rest of the
    system should not need to know whether "show" means a table in a terminal,
    a file, or a screen in a web application. This base class declares the one
    method any presentation strategy must provide, so a future presentation
    (e.g. a screen for the planner) is a new class, not a rewrite of the caller.

WHERE IMPLEMENTATIONS LIVE:
    Concrete writers live in src/adapters/, e.g. console_result_writer.py.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from use_cases.optimization_response import OptimizationResponse


class BaseResultWriter(ABC):
    """
    This is an abstract base class (ABC) - a contract pattern, the mirror
    image of BaseDataLoader on the output side: it declares what a result
    writer must do without dictating how or where. Any class that inherits
    from BaseResultWriter must provide a ``write()`` method, so callers can
    present an outcome without caring where it ends up.
    """

    @abstractmethod
    def write(self, response: OptimizationResponse) -> None:
        """Present the response to the planner.

        Args:
            response: The outcome of planning one flight. Every outcome must
                be presented, not only the successful one.
        """
