import logging
import math


def get_triangle_type_and_coords(s1, s2, s3):
    try:
        a, b, c = float(s1), float(s2), float(s3)
    except ValueError:
        logging.warning("Нечисловые входные данные")
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    if a <= 0 or b <= 0 or c <= 0:
        logging.warning("Стороны должны быть положительными")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if (a + b < c or math.isclose(a + b, c)) or \
       (a + c < b or math.isclose(a + c, b)) or \
       (b + c < a or math.isclose(b + c, a)):
        logging.warning("Условие треугольника не выполнено")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    # Сравнение сторон через math.isclose вместо ==
    ab = math.isclose(a, b)
    ac = math.isclose(a, c)
    bc = math.isclose(b, c)

    if ab and ac:
        t_type = "равносторонний"
    elif ab or ac or bc:
        t_type = "равнобедренный"
    else:
        t_type = "разносторонний"

    coords = calculate_coords(a, b, c)
    logging.debug(f"Координаты рассчитаны: {coords}")
    return t_type, coords


def calculate_coords(a, b, c):
    scale = 100.0 / max(a, b, c)

    x1, y1 = 0, 0
    x2, y2 = int(a * scale), 0

    cos_angle = (a * a + b * b - c * c) / (2 * a * b)

    # Защита от микроскопического выхода за [-1, 1] из-за погрешности float,
    # иначе math.acos вернёт nan.
    cos_angle = max(-1.0, min(1.0, cos_angle))

    angle = math.acos(cos_angle)

    x3 = int(b * scale * math.cos(angle))
    y3 = int(b * scale * math.sin(angle))

    return [(x1, y1), (x2, y2), (x3, y3)]