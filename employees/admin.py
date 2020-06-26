from django.contrib import admin

from employees.models import (
    Education,
    EmergencyContact,
    Employee,
    WorkHistory,
)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "school",
        "degree",
        "year_graduated",
    )
    list_filter = (
        "school",
        "degree",
        "year_graduated",
    )
    search_fields = (
        "employee__nickname",
        "school",
        "degree",
        "year_graduated",
    )


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "name",
        "contact_number",
    )
    search_fields = (
        "employee__nickname",
        "name",
    )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "nickname",
        "user",
        "gender",
        "date_started",
    )
    list_filter = (
        "gender",
        "is_active",
    )
    search_fields = (
        "user__first_name",
        "user__last_name",
        "nickname",
    )


@admin.register(WorkHistory)
class WorkHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "company",
        "position",
    )
    list_filter = ("position",)
    search_fields = (
        "employee",
        "company",
        "position",
    )
