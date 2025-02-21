from django.http import HttpResponseForbidden
from django.conf import settings

class BlockIPMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if ip in settings.BLOCK_IPS:
            return HttpResponseForbidden('You Are Blocked')

        return self.get_response(request)
