from django.utils.timezone import now

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        # print(f'[{now()}] Request: {request.path}  {request.method}')

        response = self.get_response(request)

        # print(f'[{now()}] Response: {request.path}  {request.method}')

        return response
