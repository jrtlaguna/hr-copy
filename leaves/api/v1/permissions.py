from rest_framework.permissions import BasePermission


class LeaveApplicationApproverPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.approvers.filter(user=request.user).exists()
