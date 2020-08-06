from django_restql.mixins import DynamicFieldsMixin
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from employees.models import (
    Employee,
    EmergencyContact,
    WorkHistory,
    Education,
)
from users.models import User
from users.api.v1.serializers import UserSerializer


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        exclude = ("employee",)


class WorkHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkHistory
        exclude = ("employee",)


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ("employee",)


class EmployeeSerializer(DynamicFieldsMixin, WritableNestedModelSerializer):
    user = UserSerializer()
    work_histories = WorkHistorySerializer(many=True, required=False)
    emergency_contacts = EmergencyContactSerializer(many=True, required=False)
    educations = EducationSerializer(many=True, required=False)

    class Meta:
        model = Employee
        fields = "__all__"
