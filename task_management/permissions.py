from rest_framework.permissions import BasePermission

class CanManageTasks(BasePermission):

    def has_permission(self, request, view):
        return request.user.role in ['Admin', 'Manager']


class IsTaskAssignee(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.role in ["Admin", "Manager"]:
            return True
        
        if request.user.role == "Employee" and request.user in obj.assigned_users.all():
            return request.method == "PATCH" and list(request.data.keys()) == ["status"]

        return False