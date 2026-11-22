from .triangle_calculator import TriangleCalculator


class Controller:
    """Контроллер бизнес-логики сквозного сценария."""

    def __init__(self, user_interface, database, notifier):
        self.ui = user_interface
        self.db = database
        self.notifier = notifier

    def run(self):
        s1, s2, s3 = self.ui.get_input()

        try:
            key = (float(s1), float(s2), float(s3))
        except ValueError:
            t_type, coords, err = TriangleCalculator.calculate(s1, s2, s3)
            result = self._format_result(t_type, coords, err)
            self.notifier.send(result)
            return result

        record = self.db.get(*key)

        if record is not None:
            t_type = record["triangle_type"]
            err = record["error_message"]
            coords = None
        else:
            t_type, coords, err = TriangleCalculator.calculate(s1, s2, s3)
            self.db.add(key[0], key[1], key[2], t_type, err)

        result = self._format_result(t_type, coords, err)
        self.notifier.send(result)
        return result

    @staticmethod
    def _format_result(t_type, coords, err):
        if err:
            return f"Ошибка: {err}"
        return f"Тип: {t_type}; Координаты: {coords}"