from rest_framework.permissions import IsAuthenticated


class LeaveApplicationPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        approver_actions = (
            "approve",
            "decline",
        )
        employee_actions = (
            "update",
            "partial_update",
            "cancel",
            "submit",
        )
        approver_employee_actions = ("retrieve",)

        if view.action in approver_actions:
            self.message = "Only approvers can view and approve the leave application."
            return request.user == obj.approver.user
        if view.action in employee_actions:
            self.message = "Only owners may update the leave application."
            return request.user == obj.employee.user
        if view.action in approver_employee_actions:
            self.message = "Only approvers and owners can view the leave application."
            return bool(request.user in (obj.employee.user, obj.approver.user))

        return False
