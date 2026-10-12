import io

from adapters.console_result_writer import ConsoleResultWriter
from domain.load import Load
from tests.builders import a_flight
from use_cases.optimization_response import OptimizationResponse


def _printed(response: OptimizationResponse) -> str:
    """Return exactly what the writer prints for a response."""
    stream = io.StringIO()
    ConsoleResultWriter(stream=stream).write(response)
    return stream.getvalue()


def _response_for_small_flight() -> OptimizationResponse:
    """A 1,000 kg flight where S1 and S3 fly, S2 is outbid and S4 can never fly."""
    flight = a_flight(
        1000,
        [
            ("S1", "Atlas Steel", 600, 3000),
            ("S2", "Bighorn Auto", 500, 2300),
            ("S3", "Cedar Pharma", 350.5, 1250.75),
            ("S4", "Dune Electronics", 1200, 9000),
        ],
        flight_id="SC101",
    )
    s1, _, s3, _ = flight.shipments
    return OptimizationResponse.loaded(Load(flight=flight, loaded=[s1, s3]))


def test_a_load_is_printed_as_one_table_with_totals():
    # ACT
    printed = _printed(_response_for_small_flight())

    # ASSERT — the whole output, exactly as the planner sees it
    assert printed == (
        "Flight SC101   weight limit 1,000 kg\n"
        "\n"
        "Shipment  Customer            Weight    Revenue  Decision\n"
        "--------  ----------------  --------  ---------  -------------------------------\n"
        "S1        Atlas Steel         600 kg     $3,000  LOADED\n"
        "S2        Bighorn Auto        500 kg     $2,300  left behind\n"
        "S3        Cedar Pharma      350.5 kg  $1,250.75  LOADED\n"
        "S4        Dune Electronics  1,200 kg     $9,000  left behind (over weight limit)\n"
        "\n"
        "Shipments      2 loaded, 2 left behind\n"
        "Revenue        $4,250.75\n"
        "Weight used    950.5 of 1,000 kg\n"
    )


def test_every_shipment_of_the_flight_appears_with_its_customer():
    # ACT
    printed = _printed(_response_for_small_flight())

    # ASSERT
    for shipment_id, customer in [
        ("S1", "Atlas Steel"),
        ("S2", "Bighorn Auto"),
        ("S3", "Cedar Pharma"),
        ("S4", "Dune Electronics"),
    ]:
        line = next(line for line in printed.splitlines() if line.startswith(shipment_id))
        assert customer in line


def test_a_shipment_heavier_than_the_weight_limit_is_told_apart_from_one_that_was_outbid():
    # ACT
    lines = _printed(_response_for_small_flight()).splitlines()

    # ASSERT
    outbid = next(line for line in lines if line.startswith("S2"))
    oversize = next(line for line in lines if line.startswith("S4"))
    assert outbid.endswith("left behind")
    assert oversize.endswith("left behind (over weight limit)")


def test_no_line_is_wider_than_a_projected_terminal():
    # ACT
    lines = _printed(_response_for_small_flight()).splitlines()

    # ASSERT — 80 columns is the classic terminal width
    assert max(len(line) for line in lines) <= 80


def test_no_shipment_fits_is_said_in_one_sentence():
    # ARRANGE
    flight = a_flight(100, [("S1", "Atlas Steel", 300, 3000)], flight_id="SC002")

    # ACT
    printed = _printed(OptimizationResponse.no_shipment_fits(flight))

    # ASSERT
    assert printed == (
        "Flight SC002   weight limit 100 kg\n"
        "\n"
        "No shipment fits on this flight: each one weighs more than the weight limit.\n"
    )


def test_invalid_input_is_said_in_one_sentence_with_the_reason():
    # ACT
    printed = _printed(OptimizationResponse.invalid_input("the flight is missing 'maxWeightKg'"))

    # ASSERT
    assert printed == "Cannot plan this flight: the flight is missing 'maxWeightKg'.\n"


def test_the_writer_prints_to_the_terminal_by_default(capsys):
    # ACT
    ConsoleResultWriter().write(OptimizationResponse.invalid_input("no data was found for flight 'SC999'"))

    # ASSERT
    assert capsys.readouterr().out == "Cannot plan this flight: no data was found for flight 'SC999'.\n"
