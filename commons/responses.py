from rest_framework.response import Response


def response(data,
             status: int = 200,
             error: dict = None):
    if not isinstance(data, (list, dict)):
        data = dict()

    return Response(
        data={
            'data': data,
            'error': error or {}
        },
        status=status
    )


def response_200(data):
    return response(data, 200)


def response_400():
    return response({}, 400)
