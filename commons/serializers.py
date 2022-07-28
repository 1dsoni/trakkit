from rest_framework.serializers import ModelSerializer


class DynamicFieldsSerializerMixin(object):
    """
    A mixin that dynamically decides which fields
    should be considered based on the following conditions:
    1. If the user has specified fields=x,y,z URL param, get those only
    2. Else, return all the fields.
    """

    def __init__(self, *args, **kwargs):
        super(DynamicFieldsSerializerMixin, self).__init__(*args, **kwargs)

        allowed_fields = set()
        existing_fields = set(self.fields.keys())

        # if fields are passed via the request as the `fields` param
        request = self.context.get('request', None)
        if not request:
            return

        query_params_fields = request.query_params.get('fields') or ''

        if not query_params_fields:
            return

        allowed_fields = allowed_fields.union(
            set(query_params_fields.split(','))
        )

        if allowed_fields:
            for field_name in existing_fields - allowed_fields:
                self.fields.pop(field_name)


class CustomModelSerializer(DynamicFieldsSerializerMixin, ModelSerializer):
    pass
