from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden


class CreateEventMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.has_perm('core.add_event'):
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden('<h1>403 Forbidden</h1>')