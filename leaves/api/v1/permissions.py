from rest_framework.permissions import IsAuthenticated


class LeaveApplicationApproverPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.user not in [approver.user for approver in obj.approvers.all()]:
            return False
        return True
