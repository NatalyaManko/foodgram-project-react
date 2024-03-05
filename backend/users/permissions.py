from rest_framework import permissions


class IsAdminPermission(permissions.BasePermission):
    """Права администратора на Добавление|Редактирование|Удаление"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_admin
            )
        return (
            request.method in permissions.SAFE_METHODS
        )