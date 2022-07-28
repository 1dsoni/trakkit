import uuid

from django.utils.deprecation import MiddlewareMixin

from .thread import (
    set_local_request_trace_id, delete_local_request_trace_id,
    get_local_request_trace_id
)


class LogTraceIdMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request_trace_id = self._get_request_trace_id(request)

        set_local_request_trace_id(request_trace_id)

    def process_response(self, request, response):
        response['X-TRACE-ID'] = get_local_request_trace_id()

        delete_local_request_trace_id()
        return response

    def _get_request_trace_id(self, request):
        return self._generate_id()

    @staticmethod
    def _generate_id():
        return uuid.uuid4().hex
