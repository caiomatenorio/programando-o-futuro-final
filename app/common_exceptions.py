class CommonException(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class SessionNotFoundException(CommonException):
    def __init__(self, message: str = "Sessão não encontrada."):
        super().__init__(message)
