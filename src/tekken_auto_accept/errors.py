class TekkenException(BaseException):
    pass


class CharacterNotFound(TekkenException):
    pass


class AlertError(TekkenException):
    pass
