
class HttpError(Exception):
    """Общая ошибка для всех исключений, которые возникают в результате запроса."""
    def __init__(self, message, error=None):
        super().__init__(message)
        self.message = message
        self.error = error


class RequestError(HttpError):
    """
    """


class ConnectionRequestError(RequestError):
    """
    """


class ConnectionRetryError(ConnectionRequestError):
    """Обертка для исключений, после которых будут производится повторные запросы."""


class ConnectionTimeout(ConnectionRequestError):
    """
    """


class HTTPResponseError(HttpError):
    """Имеет такое же значение как и ошибка из requests.HTTPError"""

    def __init__(self, message, error=None, status_code=None, response=None):
        self.status_code = status_code
        self.response = response
        super().__init__(message, error)


class HTTPResponseEntityTooLarge(HttpError):
    """
    """
