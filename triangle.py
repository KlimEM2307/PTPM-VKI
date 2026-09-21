import logging

logger = logging.getLogger(__name__)


def _is_positive_float(value: str) -> bool:
    """Проверяет, что строка — положительное вещественное число."""
    try:
        num = float(value)
    except (TypeError, ValueError):
        return False
    return num > 0


def _vertex_coordinates_for_error(code: int) -> list[tuple[int, int]]:
    """Возвращает координаты-заглушки для ошибочных случаев."""
    return [(code, code), (code, code), (code, code)]


def calculate_triangle(a_raw: str, b_raw: str, c_raw: str) -> tuple[str, list[tuple[int, int]]]:
    """
    Определяет вид треугольника и координаты его вершин.

    :param a_raw: длина стороны A (строка)
    :param b_raw: длина стороны B (строка)
    :param c_raw: длина стороны C (строка)
    :return: (тип_треугольника, список координат)
    """
    logger.debug("Вход в calculate_triangle: a=%r, b=%r, c=%r", a_raw, b_raw, c_raw)

    # --- 1. Проверка на числовой формат ---
    if not (_is_positive_float(a_raw) and _is_positive_float(b_raw) and _is_positive_float(c_raw)):
        logger.error("Невалидные (нечисловые/неположительные) данные: %r, %r, %r",
                     a_raw, b_raw, c_raw)
        return "", _vertex_coordinates_for_error(-2)

    a, b, c = float(a_raw), float(b_raw), float(c_raw)
    logger.debug("Стороны приведены к float: a=%s, b=%s, c=%s", a, b, c)

    # --- 2. Проверка условия существования треугольника ---
    if a + b <= c or a + c <= b or b + c <= a:
        logger.warning("Треугольник не существует со сторонами %s, %s, %s", a, b, c)
        return "не треугольник", _vertex_coordinates_for_error(-1)

    # --- 3. Определение типа ---
    if a == b == c:
        triangle_type = "равносторонний"
    elif a == b or a == c or b == c:
        triangle_type = "равнобедренный"
    else:
        triangle_type = "разносторонний"

    logger.info("Тип треугольника определён: %s", triangle_type)

    # --- 4. Расчёт координат вершин в поле 100x100 ---
    coords = _build_vertices(a, b, c)
    logger.info("Координаты вершин: %s", coords)
    return triangle_type, coords


def _build_vertices(a: float, b: float, c: float) -> list[tuple[int, int]]:
    """
    Строит координаты трёх вершин треугольника в поле 100x100.

    Логика:
      - кладём сторону c горизонтально от (0, y0) до (c, y0);
      - находим третью вершину по формулам косинусов;
      - масштабируем весь треугольник так, чтобы он вписался в 100x100;
      - переворачиваем Y (в изображении ось Y идёт вниз).
    """
    # Вершина A в начале координат, B — на оси X
    ax, ay = 0.0, 0.0
    bx, by = c, 0.0

    # Координаты третьей вершины C через теорему косинусов
    cos_a = (b ** 2 + c ** 2 - a ** 2) / (2 * b * c)
    # Защита от выхода за [-1, 1] из-за погрешностей float
    cos_a = max(-1.0, min(1.0, cos_a))
    sin_a = (1 - cos_a ** 2) ** 0.5

    cx = b * cos_a
    cy = b * sin_a

    # Масштабирование под поле 100x100
    max_x = max(ax, bx, cx)
    max_y = max(ay, by, cy)

    # небольшой отступ от края, чтобы точки не "прилипали"
    padding = 5.0
    scale_x = (100.0 - 2 * padding) / max_x if max_x > 0 else 1.0
    scale_y = (100.0 - 2 * padding) / max_y if max_y > 0 else 1.0
    scale = min(scale_x, scale_y)

    def to_px(x: float, y: float) -> tuple[int, int]:
        px = int(round(padding + x * scale))
        # Y переворачиваем: в экранных координатах 0 сверху
        py = int(round(100.0 - padding - y * scale))
        return px, py

    return [to_px(ax, ay), to_px(bx, by), to_px(cx, cy)]