from abc import ABC, abstractmethod


class UserInterface(ABC):
    """Абстрактный интерфейс взаимодействия с пользователем."""

    @abstractmethod
    def get_input(self):
        """Возвращает кортеж (side1, side2, side3) в виде строк."""
        ...


class ConsoleUserInterface(UserInterface):
    """Консольная реализация через input()."""

    def get_input(self):
        s1 = input("Введите сторону 1: ")
        s2 = input("Введите сторону 2: ")
        s3 = input("Введите сторону 3: ")
        return s1, s2, s3