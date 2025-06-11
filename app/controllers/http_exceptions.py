class HttpException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

        super().__init__(self.message)


class EmailAlreadyInUseException(HttpException):
    def __init__(self, message: str = "Email já está em uso."):
        super().__init__(status_code=409, message=message)
