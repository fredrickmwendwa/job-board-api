from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return response

    # anything DRF doesn't already know how to handle falls through to here
    return Response(
        {'error': 'something went wrong, please try again'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )