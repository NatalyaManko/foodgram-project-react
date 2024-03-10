from rest_framework import permissions


<<<<<<< HEAD
<<<<<<< HEAD
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
=======
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
class ReadOnly(permissions.BasePermission):
    """
    Кастомный пермишен для просмотра объекта
    незарегистрированным пользователем.
    """
    
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
    
    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()  


class IsAuthorPermission(permissions.BasePermission):
    """Права автора на Редактирование|Удаление своих объектов."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.method in permissions.SAFE_METHODS
                or obj.author == request.user
            )
        return request.method in permissions.SAFE_METHODS


class IsCurrentUserOrOwnerPermission(permissions.BasePermission):
    """
    Авторизованному пользователю доступно создание объектов.
    Автору доступны изменение и удаление своих объектов
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_authenticated
            )
        return request.method in permissions.SAFE_METHODS


class IsAuthorOrAdminPermission(permissions.BasePermission):
    """
    Права автора на Редактирование|Удаление своих объектов.
    Права администратора на Редактирование|Удаление объектов.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.author == request.user
                or request.user.is_admin)
        

#class IsOrReadOnlyAuthorOrAdminPermission(permissions.BasePermission):
    """
    Неавторизованным пользователям разрешёно Получение списка.
    Зарегистрированному пользователю разрешёно 
    Получение списка|Создание нового объекта.
    Права автора на Редактирование|Удаление своих объектов.
    Права администратора на Редактирование|Удаление.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)
        
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.author == request.user
                or request.user.is_admin)
    
#class IsUserOrAdminOrReadOnly(permissions.BasePermission):
    """
    Неавторизованному пользователю разрешён только просмотр.
    
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user == obj.id
                or request.user.is_admin
                )
<<<<<<< HEAD
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
