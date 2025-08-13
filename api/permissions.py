from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Разрешава достъп само ако request.user е owner на обекта.
    Очаква view.get_object() да върне инстанция с .owner
    """
    def has_object_permission(self, request, view, obj):
        return hasattr(obj, "owner") and obj.owner == request.user
