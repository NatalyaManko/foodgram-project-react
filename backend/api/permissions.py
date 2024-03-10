from rest_framework import permissions


class IsAuthorPermission(permissions.BasePermission):
    """Права автора на Редактирование|Удаление своих объектов"""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
        )


class IsAdminPermission(permissions.BasePermission):
    """Права администратора на Редактирование|Удаление объектов"""
    
    def has_permission(self, request, view):
#        breakpoint()
  #      if request.method in permissions.SAFE_METHODS:
  #          return True
  #      if request.method == 'POST':
  #          if request.user.is_authenticated:
  #              if request.user.is_staff:
  #                  return False
  #              return True

        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.method == 'POST'
                and not request.user.is_staff
            )
            or request.method == 'DELETE'
        )


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    """Права администратора на Создание\Редактирование\Удаление объектов"""

    def has_permission(self, request, view):
        return (
            (request.method in permissions.SAFE_METHODS
             and request.user.is_authenticated)
            or (request.user.is_authenticated
                and request.user.is_staff)
        )
