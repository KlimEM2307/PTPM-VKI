def validate_password(password: str) -> bool:
    """
    Выполняет валидацию строки пароля на соответствие политикам безопасности.
    """
    if not isinstance(password, str):
        raise TypeError("Пароль должен быть строкой")

    if " " in password:
        raise ValueError("Пароль не должен содержать пробелы")

    if not (8 <= len(password) <= 20):
        return False

    if not any(c.isupper() for c in password):
        return False

    if not any(c.islower() for c in password):
        return False

    if not any(c.isdigit() for c in password):
        return False

    special = set("!@#$%^&*")
    if not any(c in special for c in password):
        return False

    return True

#привет!