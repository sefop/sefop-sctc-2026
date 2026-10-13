"""
ROLE: Helper — announces a stage of the program as a boxed title in the log.

WHY THIS EXISTS:
    A run goes through five stages: Read data, Preprocess, Solve, Postprocess
    and Result. Announcing each one the same way lets whoever watches the
    console see where the program is. The box is drawn here, once, so every
    stage looks the same:

        #----------------------------------#
        #            Preprocess            #
        #----------------------------------#
"""

from __future__ import annotations

import logging

# Total width of the box, counting the "#" at both ends.
_BOX_WIDTH = 36


def log_stage(logger: logging.Logger, title: str) -> None:
    """Log a blank line followed by the boxed title of a stage.

    Args:
        logger: The logger of the module announcing the stage.
        title: The stage's name, e.g. "Preprocess".
    """
    inner_width = _BOX_WIDTH - 2
    rule = "#" + "-" * inner_width + "#"

    # The blank line separates this stage from the lines of the previous one.
    # It comes before the box, not after it, because a stage does not know
    # when it has logged its last line.
    logger.info("")
    logger.info(rule)
    logger.info("#" + title.center(inner_width) + "#")
    logger.info(rule)
