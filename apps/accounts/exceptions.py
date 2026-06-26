class InvalidCredentialsError(Exception):
    pass


class UserNotActiveError(InvalidCredentialsError):
    pass
