"""
ROLE: Implementation — of SolutionProvider, for the HiGHS solver technology.

WHY THIS EXISTS:
    This is the only file in the project that imports highspy — everything
    about building the model (variables, objective, constraints) and reading
    the solution back out lives here. Swapping HiGHS for another solver means
    writing one new SolutionProvider next to this one; nothing else changes.
"""

from __future__ import annotations

import logging

import highspy
import numpy as np

from domain.load import Load
from domain.shipment import Shipment
from use_cases.solving.optimization.solution_provider import SolutionProvider
from use_cases.solving.preprocessing.pre_processed_data import PreProcessedData

logger = logging.getLogger(__name__)

# A solver may report a yes/no variable as 0.9999 instead of 1. Anything above
# one half is read as "this shipment flies".
_LOADED_THRESHOLD = 0.5


class MipHighsSolutionProvider(SolutionProvider):
    """Builds the cargo knapsack model directly against highspy and solves it.

        maximize   sum(i) revenue_i * x_i
        subject to sum(i) weight_i * x_i <= max_weight_kg
                   x_i in {0, 1}

    Where x_i is 1 if shipment i flies and 0 if it is left behind.
    """

    @property
    def name(self) -> str:
        return "MIP (HiGHS)"

    def solve(self, data: PreProcessedData) -> Load | None:
        """Build, solve, and extract a Load from the MIP model.

        Args:
            data: The preprocessed flight and the shipments that can fly.

        Returns:
            A Load with the highest total revenue, or None if HiGHS did not
            reach an optimal solution.
        """
        shipments = data.feasible_shipments

        highs_model = highspy.Highs()
        # HiGHS prints a detailed log by default. The planner's console shows
        # the decision, not the solver's progress, so that log is switched off.
        highs_model.setOptionValue("output_flag", False)
        self._add_variables(shipments, highs_model)
        self._set_objective(shipments, highs_model)
        self._add_constraints(shipments, data.flight.max_weight_kg, highs_model)

        highs_model.run()
        status = highs_model.getModelStatus()
        logger.info("HiGHS terminated with status: %s", highs_model.modelStatusToString(status))

        if status != highspy.HighsModelStatus.kOptimal:
            return None
        return self._extract_load(data, highs_model)

    def _add_variables(self, shipments: list[Shipment], highs_model: highspy.Highs) -> None:
        """Add one yes/no variable per shipment, in the order of the shipments list.

        Column i of the model is the decision for shipments[i]; the objective,
        the constraint and the solution extraction all rely on that order.

        Args:
            shipments: The shipments that can fly.
            highs_model: The HiGHS model instance being built for this solve() call.
        """
        for i, shipment in enumerate(shipments):
            # Bounds 0 to 1 plus integrality make the variable binary.
            highs_model.addVar(0.0, 1.0)
            highs_model.changeColIntegrality(i, highspy.HighsVarType.kInteger)
            # Without this, HiGHS labels every column generically ("c0", "c1", ...).
            highs_model.passColName(i, self.variable_name(shipment.id))

    def _set_objective(self, shipments: list[Shipment], highs_model: highspy.Highs) -> None:
        """Set the revenue-maximization objective.

        Args:
            shipments: The shipments that can fly, in column order.
            highs_model: The HiGHS model instance being built for this solve() call.
        """
        for i, shipment in enumerate(shipments):
            highs_model.changeColCost(i, shipment.revenue_usd)
        highs_model.changeObjectiveSense(highspy.ObjSense.kMaximize)

    def _add_constraints(self, shipments: list[Shipment], max_weight_kg: float, highs_model: highspy.Highs) -> None:
        """Add the aircraft weight limit, the one hard physical limit of the model.

        Args:
            shipments: The shipments that can fly, in column order.
            max_weight_kg: The aircraft's weight limit.
            highs_model: The HiGHS model instance being built for this solve() call.
        """
        # Constraint: sum(i) weight_i * x_i <= max_weight_kg
        indices = np.arange(len(shipments), dtype=np.int32)
        weight_coeffs = np.array([s.weight_kg for s in shipments], dtype=np.float64)
        highs_model.addRow(-highspy.kHighsInf, max_weight_kg, len(indices), indices, weight_coeffs)
        highs_model.passRowName(0, "weight_limit")

    def _extract_load(self, data: PreProcessedData, highs_model: highspy.Highs) -> Load:
        """Convert the HiGHS solution back into a domain Load.

        The Load is built against the original flight, so its own validation
        re-checks the solver's answer against the real weight limit.

        Args:
            data: The preprocessed data whose feasible_shipments order matches
                the columns HiGHS solved for.
            highs_model: The HiGHS model instance that was solved.

        Returns:
            The Load made of every shipment whose variable is 1.
        """
        solution = highs_model.getSolution()
        loaded = [
            shipment
            for i, shipment in enumerate(data.feasible_shipments)
            if solution.col_value[i] > _LOADED_THRESHOLD
        ]
        return Load(flight=data.flight, loaded=loaded)

    @staticmethod
    def variable_name(shipment_id: str) -> str:
        """Return the solver-facing name of a shipment's decision variable.

        Prefixing with "load_" makes the model self-explanatory: a reader
        sees "load_S1" as the yes/no decision to load shipment S1.
        """
        return f"load_{shipment_id}"
