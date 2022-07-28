import logging

from .thread import (
    get_local_request_trace_id
)


class RequestIDFilter(logging.Filter):

    def filter(self, record):
        record.request_trace_id = get_local_request_trace_id()
        return True
