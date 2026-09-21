import logging
import os
import sys

from triangle import calculate_triangle


def setup_logging() -> None:
    os.makedirs("logs", exist_ok=True)

    log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/file_txt.log", encoding="utf-8"),
        ],
    )


def main() -> None:
    setup_logging()
    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")

    requests = [
        ("3", "3", "3"),          # равносторонний
        ("3", "4", "5"),          # разносторонний
        ("5", "5", "8"),          # равнобедренный
        ("1", "2", "10"),         # не треугольник
        ("abc", "2", "3"),        # нечисловые данные
        ("-1", "2", "3"),         # отрицательное число
        ("4.5", "4.5", "6"),      # равнобедренный (float)
    ]

    for a, b, c in requests:
        logging.info("--- Новый запрос: a=%s, b=%s, c=%s ---", a, b, c)
        try:
            ttype, coords = calculate_triangle(a, b, c)
            logging.info(
                "УСПЕШНЫЙ ЗАПРОС | a=%s b=%s c=%s | тип=%r | координаты=%s",
                a, b, c, ttype, coords,
            )
        except Exception:
            logging.exception(
                "НЕУСПЕШНЫЙ ЗАПРОС | a=%s b=%s c=%s | непредвиденная ошибка", a, b, c
            )

    logging.info("Приложение завершено")


if __name__ == "__main__":
    main()