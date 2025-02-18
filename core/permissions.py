from django.http import HttpResponseForbidden

def event_administrator(function):

    def wrapper(request, *args, **kwargs):
        if request.user.has_perm('core.add_event'):
            return function(request, *args, **kwargs)

        return HttpResponseForbidden('You do not have permission to perform this action.')

    return wrapper