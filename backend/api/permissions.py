from rest_framework import permissions


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
