# TODO write the exceptions to be raised by the various services'
#  interfaces/apis, the exc should be able to identify what broke in the
#  integration

# TODO use this as the base exception throughout the project


class BaseApiException(Exception):
    status_code = 500
    default_display_message = 'Operation failed'

    def __init__(self,
                 error_code: str,
                 api_message: str = '',
                 extra: dict = None):
        self.error_code = error_code
        self.api_message = api_message
        self.extra = extra
        self.message = f'{self.default_display_message}: {error_code}'

    def __str__(self):
        return str(self.message)


class ExternalApiError(BaseApiException):
    status_code = 400
    default_display_message = 'Operation failed'


class SimpleApiError(BaseApiException):
    status_code = 400
    default_display_message = 'Operation failed'
