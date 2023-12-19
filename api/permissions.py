from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff is True


class IsCommentOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.created_by == request.user or request.user.is_admin:
            return True
        return False

