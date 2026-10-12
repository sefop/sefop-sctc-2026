"""
ROLE: Abstract Base Class — contract that every solution provider must follow.

WHY THIS EXISTS:
    Solution providers (the MIP solver, brute-force enumeration) are pluggable
    implementations of this interface so Orchestrator can run any of them
    through a single ``solve()`` call without knowing which one it was given.

    This is an internal solving-pipeline contract, not a public port: it lives
    inside use_cases/solving/ because only the solving pipeline's own
    collaborators (Orchestrator, MipHighsSolutionProvider,
    EnumerationSolutionProvider) ever implement or call it — it is not
    something adapters/ implement the way use_cases/ports/ contracts are.

WHERE IMPLEMENTATIONS LIVE:
    src/use_cases/solving/optimization/<technology>/, e.g. mip_highs/mip_highs_solution_provider.py.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from domain.load import Load
from use_cases.solving.preprocessing.pre_processed_data import PreProcessedData


class SolutionProvider(ABC):
    """
    An abstract base class (ABC) is like a contract: it declares a set of
    methods that every provider **must** implement, but says nothing about
    *how*. Any class that inherits from ``SolutionProvider`` is forced to
    provide ``solve()`` and ``name``, so Orchestrator can call ``solve()``
    and log which provider ran, without caring whether an exact MIP solver
    or brute-force enumeration is doing the work behind the scenes.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-friendly label for this provider, used in Orchestrator's log.

        Returns:
            A short technology label, e.g. "MIP (HiGHS)".
        """

    @abstractmethod
    def solve(self, data: PreProcessedData) -> Load | None:
        """Choose the shipments that fly for the given data.

        Args:
            data: The preprocessed flight and the shipments that can fly.

        Returns:
            A Load with the highest total revenue that respects the weight
            limit, or None if the provider could not produce one. When
            several loads share the highest revenue, any one of them may be
            returned.
        """
