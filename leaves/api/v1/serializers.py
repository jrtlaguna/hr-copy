from rest_framework import serializers

from employees.models import Employee
from leaves.models import LeaveAllocation, LeaveType


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = "__all__"


class LeaveTypeRelationSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="leaves-v1:leave-types-detail")

    class Meta:
        model = LeaveType
        fields = (
            "id",
            "url",
            "name",
        )


class EmployeeRelationSerializer(serializers.ModelSerializer):
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


class LeaveAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveAllocation
        fields = "__all__"

    def to_representation(self, instance):
        request = self.context.get("request")
        if request.method == "GET":
            self.fields["employee"] = EmployeeRelationSerializer()
            self.fields["leave_type"] = LeaveTypeRelationSerializer()
        return super().to_representation(instance)
