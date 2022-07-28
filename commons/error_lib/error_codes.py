from dataclasses import dataclass

default_user_message = 'Something went wrong! Please try again.'


@dataclass
class ErrorCodeMeta:
    error_code: str
    user_message: str = default_user_message


undef_error = 'undef_error'
request_timed_out = 'request_timed_out'
