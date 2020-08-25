from rest_framework.permissions import IsAuthenticated


class LeaveApplicationApproverPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.approvers.filter(user=request.user).exists()
