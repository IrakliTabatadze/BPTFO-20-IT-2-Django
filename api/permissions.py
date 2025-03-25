from rest_framework.permissions import BasePermission

class HasEventViewPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.has_perm('core.view_event')