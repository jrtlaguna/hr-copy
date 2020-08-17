from django_filters import FilterSet, filters

from django.db.models import Q

from leaves.models import (
    LeaveAllocation,
    LeaveApplication,
    LeaveType,
)


class LeaveTypeFilter(FilterSet):
    search = filters.CharFilter(method="_multi_search", label="name")
    is_active = filters.BooleanFilter(field_name="is_active", label="is active")

    def _multi_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value))

    class Meta:
        model = LeaveType
        fields = []


class LeaveAllocationFilter(FilterSet):
    is_active = filters.BooleanFilter(field_name="is_active", label="is active")
    employee = filters.CharFilter(method="employee_search", label="employee")
    leave_type = filters.CharFilter(method="leave_type_search", label="type")

    def employee_search(self, queryset, name, value):
        return queryset.filter(
            Q(employee__user__email__icontains=value)
            | Q(employee__user__first_name__icontains=value)
            | Q(employee__user__middle_name__icontains=value)
            | Q(employee__user__last_name__icontains=value)
            | Q(employee__nickname__icontains=value)
        )

    def leave_type_search(self, queryset, name, value):
        return queryset.filter(Q(leave_type__name__icontains=value))

    class Meta:
        model = LeaveAllocation
        fields = []


class LeaveApplicationFilter(FilterSet):
    status = filters.ChoiceFilter(
        choices=LeaveApplication.STATUS_CHOICES, label="status"
    )
    approver = filters.CharFilter(method="employee_search", label="approver")
    employee = filters.CharFilter(method="employee_search", label="employee")
    leave_type = filters.CharFilter(method="leave_type_search", label="type")

    def employee_search(self, queryset, name, value):
        return queryset.filter(
            Q(employee__user__email__icontains=value)
            | Q(employee__user__first_name__icontains=value)
            | Q(employee__user__middle_name__icontains=value)
            | Q(employee__user__last_name__icontains=value)
            | Q(employee__nickname__icontains=value)
        )

    def leave_type_search(self, queryset, name, value):
        return queryset.filter(Q(leave_type__name__icontains=value))

    class Meta:
        model = LeaveApplication
        fields = []
