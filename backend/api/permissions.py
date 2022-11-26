from rest_framework.permissions import BasePermission, SAFE_METHODS 

from users.models import UserRole


class IsAuthorOrAdminOrReadOnly(BasePermission):
    """Редактирование доступно только автору либо админу."""    
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.role == UserRole.ADMIN)
