from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers

from employees.models import (
    Employee,
    EmergencyContact,
    WorkHistory,
    Education,
)
from users.api.serializers import UserSerializer


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = "__all__"


class WorkHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkHistory
        fields = "__all__"


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"


class EmployeeSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    user = UserSerializer()
    work_histories = WorkHistorySerializer(many=True,)
    emergency_contacts = EmergencyContactSerializer(many=True,)
    educations = EducationSerializer(many=True,)

    class Meta:
        model = Employee
        fields = "__all__"
