from __future__ import annotations
from collections import defaultdict
from typing import Sequence
from ..models import ProductRecord
from ..reporting import Report, register_report

@register_report
class AverageRatingReport(Report):
    """Считает средний рейтинг по брендам и сортирует по убыванию."""
    name = "average-rating"
    def generate(self, products: Sequence[ProductRecord]) -> list[dict[str, object]]:
        totals: dict[str, dict[str, float]] = defaultdict(lambda: {"total": 0.0, "count": 0.0})

        for record in products:
            stats = totals[record.brand]
            stats["total"] += record.rating
            stats["count"] += 1

        brand_averages: list[tuple[str, float]] = []
        for brand, stats in totals.items():
            average = stats["total"] / stats["count"]
            brand_averages.append((brand, average))

        brand_averages.sort(key=lambda item: (-item[1], item[0]))

        return [{"brand": brand, "rating": round(average, 2)} for brand, average in brand_averages]
