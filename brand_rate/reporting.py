from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Mapping, Sequence
from .models import ProductRecord

class Report(ABC):
    """Отчёт, преобразующий записи товаров в табличный вид."""
    name: str
    @abstractmethod
    def generate(self, products: Sequence[ProductRecord]) -> list[Mapping[str, object]]:
        """Возвращает список словарей, готовых к выводу в таблице."""


class UnknownReportError(LookupError):
    def __init__(self, name: str, available: Sequence[str]):
        available_display = ", ".join(available) if available else "нет"
        message = f"Неизвестный отчёт '{name}'. Доступные варианты: {available_display}"
        super().__init__(message)
        self.name = name
        self.available = list(available)


class ReportRegistry:
    """Хранит все зарегистрированные классы отчётов."""
    def __init__(self) -> None:
        self._reports: dict[str, type[Report]] = {}

    def register(self, report_cls: type[Report]) -> type[Report]:
        name = getattr(report_cls, "name", "").strip()
        if not name:
            raise ValueError("У класса отчёта должно быть непустое поле 'name'.")
        self._reports[name] = report_cls
        return report_cls

    def create(self, name: str) -> Report:
        try:
            report_cls = self._reports[name]
        except KeyError as exc:
            raise UnknownReportError(name, self.available_reports()) from exc
        return report_cls()

    def available_reports(self) -> list[str]:
        return sorted(self._reports.keys())

registry = ReportRegistry()

def register_report(report_cls: type[Report]) -> type[Report]:
    """Декоратор для регистрации отчёта в общем реестре."""
    return registry.register(report_cls)

__all__ = ["Report", "ReportRegistry", "register_report", "registry", "UnknownReportError"]