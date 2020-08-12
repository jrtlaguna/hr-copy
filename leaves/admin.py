from django.contrib import admin

from leaves.models import (
    LeaveAllocation,
    LeaveApplication,
    LeaveType,
)


@admin.register(LeaveAllocation)
class LeaveAllocationAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "leave_type",
        "from_date",
        "to_date",
        "count",
    )
    list_filter = ("leave_type",)
    list_select_related = (
        "employee",
        "leave_type",
    )
    raw_id_fields = (
        "employee",
        "leave_type",
    )
    readonly_fields = (
        "created",
        "modified",
    )
    search_fields = (
        "employee__user__first_name",
        "employee__user__last_name",
        "employee__nickname",
    )


@admin.register(LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "approver",
        "employee",
        "leave_type",
        "from_date",
        "to_date",
        "status",
    )
    list_filter = (
        "leave_type",
        "status",
    )
    list_select_related = (
        "approver",
        "employee",
        "leave_type",
    )
    raw_id_fields = (
        "approver",
        "employee",
        "leave_type",
    )
    readonly_fields = (
        "created",
        "modified",
    )
    search_fields = (
        "employee__user__first_name",
        "employee__user__last_name",
        "employee__nickname",
        "name",
    )


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_paid",
        "is_optional",
        "is_carry_forwarded",
        "is_convertible_to_cash",
        "is_carry_forwarded",
    )
    list_filter = (
        "is_paid",
        "is_optional",
        "is_carry_forwarded",
        "is_convertible_to_cash",
        "is_carry_forwarded",
    )
    readonly_fields = (
        "created",
        "modified",
    )
    search_fields = ("name",)
