from abc import ABC, abstractmethod


class Notifier(ABC):
    """Абстрактный интерфейс сторонней зависимости."""

    @abstractmethod
    def send(self, message: str) -> bool:
        """Имитация отправки. Возвращает True при успехе."""
        ...


class ConsoleNotifier(Notifier):
    """Имитация отправки на внешний сервер (просто печать)."""

    def send(self, message: str) -> bool:
        print(f"[SERVER] {message}")
        return True