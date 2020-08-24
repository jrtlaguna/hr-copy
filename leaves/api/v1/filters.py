from django_filters import FilterSet, filters

from django.db.models import Q

from leaves.models import (
    LeaveAllocation,
    LeaveApplication,
    LeaveType,
)


class LeaveTypeFilter(FilterSet):
    class Meta:
        model = LeaveType
        fields = ["name", "is_active"]


class LeaveAllocationFilter(FilterSet):
    employee = filters.CharFilter(method="employee_search", label="employee")

    class Meta:
        model = LeaveAllocation
        fields = [
            "is_active",
            "leave_type",
        ]

    def employee_search(self, queryset, name, value):
        return queryset.filter(
            Q(employee__user__email__icontains=value)
            | Q(employee__user__first_name__icontains=value)
            | Q(employee__user__middle_name__icontains=value)
            | Q(employee__user__last_name__icontains=value)
            | Q(employee__nickname__icontains=value)
        )


class LeaveApplicationFilter(FilterSet):
    employee = filters.CharFilter(method="employee_search", label="employee")
    approvers = filters.CharFilter(method="approver_search", label="approvers")

    class Meta:
        model = LeaveApplication
        fields = [
            "leave_type",
            "status",
        ]

    def employee_search(self, queryset, name, value):
        return queryset.filter(
            Q(employee__user__email__icontains=value)
            | Q(employee__user__first_name__icontains=value)
            | Q(employee__user__middle_name__icontains=value)
            | Q(employee__user__last_name__icontains=value)
            | Q(employee__nickname__icontains=value)
        )

    def approver_search(self, queryset, name, value):
        return queryset.filter(
            Q(approvers__user__email__icontains=value)
            | Q(approvers__user__first_name__icontains=value)
            | Q(approvers__user__middle_name__icontains=value)
            | Q(approvers__user__last_name__icontains=value)
            | Q(approvers__nickname__icontains=value)
        )
