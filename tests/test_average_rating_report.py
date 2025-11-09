from brand_rate.models import ProductRecord
from brand_rate.reports.average_rating import AverageRatingReport


def test_average_rating_report_orders_by_score_and_name():
    products = [
        ProductRecord(name="a", brand="apple", price=0.0, rating=4.2),
        ProductRecord(name="b", brand="apple", price=0.0, rating=4.8),
        ProductRecord(name="c", brand="samsung", price=0.0, rating=4.5),
        ProductRecord(name="d", brand="samsung", price=0.0, rating=4.5),
        ProductRecord(name="e", brand="xiaomi", price=0.0, rating=4.1),
    ]

    report = AverageRatingReport()
    rows = report.generate(products)

    assert rows == [
        {"brand": "apple", "rating": 4.5},
        {"brand": "samsung", "rating": 4.5},
        {"brand": "xiaomi", "rating": 4.1},
    ]
