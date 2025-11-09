from __future__ import annotations
import csv
from pathlib import Path
from typing import Sequence
from .models import ProductRecord

class CSVProductReader:
    """Загружает записи товаров из CSV-файлов."""
    REQUIRED_COLUMNS = {"name", "brand", "price", "rating"}
    def read_many(self, paths: Sequence[str]) -> list[ProductRecord]:
        if not paths:
            raise ValueError("Нужно указать хотя бы один файл с данными.")

        records: list[ProductRecord] = []
        for path in paths:
            records.extend(self.read(path))
        return records

    def read(self, path: str | Path) -> list[ProductRecord]:
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(file_path)

        with file_path.open("r", encoding="utf-8", newline="") as file_obj:
            reader = csv.DictReader(file_obj)
            fieldnames = set(reader.fieldnames or [])
            missing = self.REQUIRED_COLUMNS - fieldnames
            if missing:
                missing_list = ", ".join(sorted(missing))
                raise ValueError(f"В файле {file_path} отсутствуют колонки: {missing_list}")

            return [ProductRecord.from_row(row) for row in reader]