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
        return True if view.action == 'retrieve' else False
