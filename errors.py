class ApiError(Exception):
    status_code = 400

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code


#Missing resources like a missing task
class NotFoundError(ApiError):
    def __init__(self, message: str = "resource not found"):
        super().__init__(message, status_code=404)


class BadRequestError(ApiError):
    def __init__(self, message: str = "bad request"):
        super().__init__(message, status_code=400)