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
    class Meta:
        model = LeaveAllocation
        fields = [
            "is_active",
            "employee",
            "leave_type",
        ]


class LeaveApplicationFilter(FilterSet):
    class Meta:
        model = LeaveApplication
        fields = [
            "approver",
            "employee",
            "leave_type",
            "status",
        ]
