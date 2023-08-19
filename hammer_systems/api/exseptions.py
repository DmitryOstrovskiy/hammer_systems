class APIErrors(Exception):
    """базовый класс для всех исключений."""
    pass


class CodeDoesNotExist(APIErrors):
    """Имя пользователя не существет в базе."""
    pass
