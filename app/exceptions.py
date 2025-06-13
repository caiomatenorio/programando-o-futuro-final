# Common exceptions for the application


class SessionNotFoundException(Exception):
    def __init__(self, message: str = "Sessão não encontrada."):
        self.message = message
        super().__init__(self.message)


# HTTP exceptions for the application


class HttpException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

        super().__init__(self.message)


class EmailAlreadyInUseException(HttpException):
    def __init__(self, message: str = "Email já está em uso."):
        super().__init__(status_code=409, message=message)


class UserNotFoundException(HttpException):
    def __init__(self, message: str = "Usuário não encontrado."):
        super().__init__(status_code=404, message=message)


class InvalidCredentialsException(HttpException):
    def __init__(self, message: str = "Credenciais inválidas."):
        super().__init__(status_code=401, message=message)


class UnauthorizedException(HttpException):
    def __init__(self, message: str = "Não autorizado."):
        super().__init__(status_code=401, message=message)
