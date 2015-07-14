class FCC4DException(Exception):
    def __init__(self, message=None):
        super().__init__(message)
        self.message = message


class ApiPermissionException(FCC4DException):
    pass


class ApiServerError(FCC4DException):
    pass


class ApiValueError(FCC4DException):
    pass
