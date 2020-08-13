from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from employees.models import Employee
from leaves.models import LeaveAllocation, LeaveType


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = "__all__"


class LeaveTypeLinkSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="leaves-v1:leave-types-detail")

    class Meta:
        model = LeaveType
        fields = (
            "id",
            "url",
            "name",
        )


class EmployeeLinkSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="employees-v1:employees-detail"
    )
    first_name = serializers.CharField(read_only=True, source="user.first_name")
    middle_name = serializers.CharField(read_only=True, source="user.middle_name")
    last_name = serializers.CharField(read_only=True, source="user.last_name")
    email = serializers.CharField(read_only=True, source="user.email")

    class Meta:
        model = Employee
        fields = (
            "id",
            "url",
            "first_name",
            "middle_name",
            "last_name",
            "email",
        )


class CreateUpdateLeaveAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveAllocation
        fields = "__all__"


class LeaveAllocationSerializer(serializers.ModelSerializer):
    leave_type = LeaveTypeLinkSerializer(read_only=True)
    employee = EmployeeLinkSerializer(read_only=True)

    class Meta:
        model = LeaveAllocation
        fields = "__all__"

