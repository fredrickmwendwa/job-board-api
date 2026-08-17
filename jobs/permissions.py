from rest_framework import permissions


class IsCompanyOwner(permissions.BasePermission):
    """
    only lets the company that posted a job edit or delete it
    everyone else can only read (GET requests)
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.posted_by == request.user