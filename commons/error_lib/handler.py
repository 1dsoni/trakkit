import logging

from .error_codes import undef_error
from .exceptions import BaseApiException
from ..responses import response

logger = logging.getLogger(__name__)

DEFAULT_STATUS_CODE = 500


def custom_exception_handler(exc, context):
    logger.exception(exc)

    status_code = DEFAULT_STATUS_CODE
    error_code = undef_error
    api_message = ''
    extra = None

    if issubclass(exc.__class__, BaseApiException):
        status_code = getattr(exc, 'status_code', DEFAULT_STATUS_CODE)
        error_code = getattr(exc, 'error_code', undef_error)
        api_message = getattr(exc, 'api_message', '')
        extra = getattr(exc, 'extra', None)

    return response(
        data={},
        status=status_code,
        error={
            'error_code': error_code,
            'extra': extra or {},
            'message': api_message
        }
    )
