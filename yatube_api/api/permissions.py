from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает менять объект только его автору.
    Остальным — только методы GET, HEAD, OPTIONS (безопасные методы).
    """
    def has_object_permission(self, request, view, obj):
        # Разрешаем читать всем аутентифицированным
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешаем менять/удалять, только если это автор объекта
        return obj.author == request.user
