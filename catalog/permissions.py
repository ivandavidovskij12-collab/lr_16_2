from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешает GET всем, остальные методы только администраторам"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsOwnerOrAdmin(permissions.BasePermission):
    """Разрешает доступ только владельцу или администратору"""
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'cart') and hasattr(obj.cart, 'user'):
            return obj.cart.user == request.user
        return False

class IsAdminUser(permissions.BasePermission):
    """Только для администраторов"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_staff