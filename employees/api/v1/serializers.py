from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers

from core.serializers import CustomWritableNestedModelSerializer
from employees.models import (
    Employee,
    EmergencyContact,
    WorkHistory,
    Education,
)
from users.api.v1.serializers import UserSerializer


class EmergencyContactSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        exclude = ("employee",)


class WorkHistorySerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = WorkHistory
        exclude = ("employee",)


class EducationSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ("employee",)


class EmployeeSerializer(DynamicFieldsMixin, CustomWritableNestedModelSerializer):
    user = UserSerializer(partial=True)
    work_histories = WorkHistorySerializer(many=True, required=False)
    emergency_contacts = EmergencyContactSerializer(many=True, required=False)
    educations = EducationSerializer(many=True, required=False)

    class Meta:
        model = Employee
        fields = "__all__"
