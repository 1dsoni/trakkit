from drf_yasg.inspectors import SwaggerAutoSchema
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from .error_lib.handler import custom_exception_handler
from .paginations import CustomPageNumberPagination


class CustomAutoSchema(SwaggerAutoSchema):
    """
    Removed all the code to generate the method summary and parsing of doc
    string.
    """

    def get_summary_and_description(self):
        """
        Returns the docstring of the action to show the api description.
        """
        view = self.view
        method_name = getattr(view, 'action', self.method.lower())
        return '', getattr(view, method_name, None).__doc__


class BaseApiViewSet(GenericViewSet):
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    pagination_class = CustomPageNumberPagination
    swagger_schema = CustomAutoSchema

    lookup_field = "ref_id"

    def perform_authentication(self, request):
        # dont need native django authentication
        return

    def get_exception_handler(self):
        """
        Returns the exception handler that this view uses.
        """
        return custom_exception_handler
