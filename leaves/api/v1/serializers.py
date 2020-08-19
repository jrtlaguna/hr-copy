from datetime import datetime

from django_restql.fields import NestedField
from django_restql.mixins import DynamicFieldsMixin
from django_restql.serializers import NestedModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import APIException


from employees.api.v1.serializers import EmployeeSerializer
from employees.models import Employee
from leaves.models import (
    LeaveAllocation,
    LeaveApplication,
    LeaveType,
)


class LeaveTypeSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = "__all__"


class LeaveAllocationSerializer(DynamicFieldsMixin, NestedModelSerializer):
    leave_type = NestedField(LeaveTypeSerializer, accept_pk=True)
    employee = NestedField(EmployeeSerializer, accept_pk=True)

    class Meta:
        model = LeaveAllocation
        fields = "__all__"


class LeaveApplicationSerializer(DynamicFieldsMixin, NestedModelSerializer):
    approver = NestedField(EmployeeSerializer, accept_pk=True)
    leave_type = NestedField(LeaveTypeSerializer, accept_pk=True)
    employee = NestedField(EmployeeSerializer, accept_pk=True)

    class Meta:
        model = LeaveApplication
        fields = "__all__"

    def validate(self, attrs):
        request = self.context.get("request")

        employee = attrs.get("employee")
        leave_type = attrs.get("leave_type")
        from_date = attrs.get("from_date")
        to_date = attrs.get("to_date")

        if self.partial:
            employee = attrs.get("employee", self.instance.employee)
            leave_type = attrs.get("leave_type", self.instance.leave_type)
            from_date = attrs.get("from_date", self.instance.from_date)
            to_date = attrs.get("to_date", self.instance.to_date)

        if from_date > to_date:
            raise serializers.ValidationError("End date must be after start date")
        leave_allocations = (
            employee.leave_allocations.filter(
                leave_type=leave_type, is_active=True, count__gt=0
            )
            .filter(from_date__lte=from_date, to_date__gte=to_date)
            .all()
        )
        if not leave_allocations:
            raise serializers.ValidationError("Insufficient Leave Allocation")
        return super().validate(attrs)
