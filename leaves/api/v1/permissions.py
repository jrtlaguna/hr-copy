from rest_framework.permissions import IsAuthenticated


class LeaveApplicationPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        approver_actions = (
            "retrieve",
            "approve",
            "decline",
        )

        employee_actions = (
            "retrieve",
            "update",
            "partial_update",
            "cancel",
            "submit",
        )

        if view.action in approver_actions:
            if request.user == obj.approver.user:
                self.message = (
                    "Only approvers can view and approve the leave application."
                )
                return True
        if view.action in employee_actions:
            if request.user == obj.employee.user:
                self.message = "Only owners may update the leave application."
                return True

        return False
