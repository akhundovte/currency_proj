import requests
import time
import logging

from .exceptions import (
    HttpError, ConnectionRequestError, ConnectionTimeout,
    HTTPResponseError, ConnectionRetryError
    )


TIMEOUT_CONNECT = 30
TIMEOUT_READ = 30


class ConnectorRequests:
    """Коннектор на основе библиотеки requests."""

    def __init__(
        self,
        timeout=None,
        headers=None,
        login=None,
        password=None,
        logger=None,
        max_retries=3,
        retry_on_status=(502, 503, 504, )
    ):
        if timeout is None:
            timeout = (TIMEOUT_CONNECT, TIMEOUT_READ)
        self._logger = logger if logger is not None else logging.getLogger(__name__)
        self._max_retries = max_retries
        self._retry_on_status = retry_on_status
        self.session = requests.Session()
        self.session.headers = headers or {}
        self._timeout = timeout
        self._auth = None
        self._set_auth_by_login(login, password)

    def perform_request(self, url, method='GET', login=None, password=None, **kwargs):
        """
        Совершение запроса с повторениями в случае ошибок.
        """
        self._set_auth_by_login(login, password)
        for attempt in range(self._max_retries + 1):
            if attempt > 0:
                msg = f"Попытка номер {attempt} для {url}"
                self._logger.info(msg)
            try:
                # add a delay before attempting the next retry
                # 0, 1, 3, 7, etc...
                delay = 2**attempt - 1
                time.sleep(delay)
                response = self._request(url, method, **kwargs)
            except HttpError as e:
                retry = False
                if isinstance(e, (ConnectionRetryError, ConnectionTimeout)):
                    retry = True
                elif isinstance(e, HTTPResponseError) and e.status_code in self._retry_on_status:
                    retry = True
                if retry:
                    if attempt == self._max_retries:
                        raise e
                else:
                    raise e
            else:
                return response

    def _set_auth_by_login(self, login, password):
        if login is not None and password is not None:
            self._auth = requests.auth.HTTPBasicAuth(login, password)

    def _request(self, url, method, **kwargs):
        """Запрос."""
        try:
            response = self.session.request(
                method, url,
                timeout=self._timeout, auth=self._auth,
                **kwargs
                )

            if 400 <= response.status_code < 500:
                http_error_msg = f"{response.status_code} Client Error for url: {url}"
                raise HTTPResponseError(
                    http_error_msg, status_code=response.status_code, response=response)

            elif 500 <= response.status_code < 600:
                http_error_msg = f"{response.status_code} Server Error for url: {url}"
                raise HTTPResponseError(
                    http_error_msg, status_code=response.status_code, response=response)

            return response

        except Exception as e:
            if isinstance(e, HttpError):  # наше базовое исключение
                raise e
            # на TimeoutError реагируем повторными запросами
            if isinstance(e, requests.Timeout):
                raise ConnectionTimeout('TIMEOUT %s' % str(e), error=e)

            # на данные ошибки не делаем повторных запросов
            if isinstance(e, requests.exceptions.SSLError):
                raise ConnectionRequestError(str(e), error=e)

            # на все остальные ошибки делаем retry, RequestException - базовая ошибка requests
            if isinstance(e, requests.RequestException):
                if hasattr(e, 'message') and e.message is None:
                    str_error = repr(e)
                else:
                    # у ServerDisconnectedError обычно message = None, поэтому str(e) дает строку 'None'
                    # поэтому берем тип ошибки
                    str_error = str(e)
                raise ConnectionRetryError(str_error, error=e)
            raise e

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
