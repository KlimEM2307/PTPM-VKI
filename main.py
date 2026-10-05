import logging
import sys
from triangle import get_triangle_type_and_coords


def main():
    log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/file_txt.log", encoding="utf-8")
        ]
    )

    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")
    while True:
        try:
            a = input("Введите сторону A: ")
            b = input("Введите сторону B: ")
            c = input("Введите сторону C: ")

            logging.info(f"Запрос: A={a}, B={b}, C={c}")

            triangle_type, coords = get_triangle_type_and_coords(a, b, c)

            logging.info(f"Результат: тип='{triangle_type}', координаты={coords}")
            print(f"Тип треугольника: {triangle_type}")
            print(f"Координаты вершин: {coords}")

        except Exception as ex:
            logging.error("Неуспешный запрос")
            logging.exception("Трассировка стека:")
            print("Произошла ошибка при обработке запроса")


if __name__ == "__main__":
    main()