from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and response.status_code == 500:
        response.data = {
            "detail": "Token muddati tugagan. Yangi token oling yoki qayta tizimga kiring."
        }

    return response
