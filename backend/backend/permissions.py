from rest_framework import permissions


class IsAuthorPermission(permissions.BasePermission):
    """Права автора на Редактирование|Удаление своих объектов"""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
        )


class CanViewUserProfile(permissions.BasePermission):
    """Права на просмотр страниц пользователей"""

    def has_permission(self, request, view):
        if view.action == 'list':
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True

        return False
