"""
ROLE: Implementation of a post-processing step for the solving pipeline.

WHY THIS EXISTS:
    This module sits at the end of the optimization pipeline. The default
    implementation puts the loaded shipments back in the order the planner
    listed them, so output is deterministic and readable — override it to add
    further steps, such as extra checks on the load or enriching the result,
    without touching the provider that produced the load.
"""

from __future__ import annotations

from domain.load import Load


class PostProcess:
    """Post-processing step after provider execution.

    The default `run()` orders the loaded shipments as they appear on the
    flight. Override this class to add custom post-processing logic.
    """

    def run(self, load: Load) -> Load:
        """Order the loaded shipments as the flight lists them.

        A provider may return the loaded shipments in any order. Following
        the flight's own order means the planner reads the result in the
        same sequence as the input.
        """
        position = {shipment.id: index for index, shipment in enumerate(load.flight.shipments)}
        ordered = sorted(load.loaded, key=lambda shipment: position[shipment.id])
        return Load(flight=load.flight, loaded=ordered)
