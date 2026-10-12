from domain.load import Load
from tests.builders import a_flight, loaded_ids
from use_cases.solving.postprocessing.postprocessing import PostProcess


def test_loaded_shipments_are_listed_in_the_order_of_the_flight():
    # ARRANGE — a provider returned the loaded shipments out of order
    flight = a_flight(
        1000,
        [("S1", "Atlas Steel", 300, 3000), ("S2", "Bighorn Auto", 250, 2300), ("S3", "Cedar Pharma", 100, 800)],
    )
    s1, s2, s3 = flight.shipments
    unordered = Load(flight=flight, loaded=[s3, s1, s2])

    # ACT
    ordered = PostProcess().run(unordered)

    # ASSERT
    assert loaded_ids(ordered) == ["S1", "S2", "S3"]


def test_ordering_changes_neither_revenue_nor_weight():
    # ARRANGE
    flight = a_flight(1000, [("S1", "Atlas Steel", 300, 3000), ("S2", "Bighorn Auto", 250, 2300)])
    s1, s2 = flight.shipments
    unordered = Load(flight=flight, loaded=[s2, s1])

    # ACT
    ordered = PostProcess().run(unordered)

    # ASSERT
    assert ordered.total_revenue_usd == unordered.total_revenue_usd
    assert ordered.total_weight_kg == unordered.total_weight_kg
