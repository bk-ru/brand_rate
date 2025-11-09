from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping

@dataclass(frozen=True, slots=True)
class ProductRecord:
    """Описывает строку товара считанную из CSV."""
    name: str
    brand: str
    price: float
    rating: float
    
    @classmethod
    def from_row(cls, row: Mapping[str, str]) -> "ProductRecord":
        """Создаёт запись товара из строки CSV."""
        try:
            name_raw = row["name"]
            brand_raw = row["brand"]
            price_raw = row["price"]
            rating_raw = row["rating"]
        except KeyError as exc:
            raise ValueError(f"Отсутствует обязательная колонка: {exc.args[0]}") from exc

        name = name_raw.strip()
        brand = brand_raw.strip().lower()

        try:
            price = float(price_raw)
            rating = float(rating_raw)
        except (TypeError, ValueError) as exc:
            raise ValueError("Цена и рейтинг должны быть числом") from exc

        return cls(name=name, brand=brand, price=price, rating=rating)