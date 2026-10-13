import logging

from use_cases.stage_log import log_stage


def test_a_stage_is_announced_as_a_boxed_title_after_a_blank_line(caplog):
    # ARRANGE
    logger = logging.getLogger("stage_log_test")

    # ACT
    with caplog.at_level(logging.INFO):
        log_stage(logger, "Preprocess")

    # ASSERT
    assert caplog.messages == [
        "",
        "#----------------------------------#",
        "#            Preprocess            #",
        "#----------------------------------#",
    ]


def test_every_box_has_the_same_width_whatever_the_title(caplog):
    # ARRANGE
    logger = logging.getLogger("stage_log_test")

    # ACT
    with caplog.at_level(logging.INFO):
        for title in ["Read data", "Preprocess", "Solve", "Postprocess", "Result"]:
            log_stage(logger, title)

    # ASSERT
    assert {len(line) for line in caplog.messages if line} == {36}
