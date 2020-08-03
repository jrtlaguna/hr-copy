from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers

from employees.models import (
    Employee,
    EmergencyContact,
    WorkHistory,
    Education,
)
from users.api.v1.serializers import UserSerializer


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
    work_histories = WorkHistorySerializer(many=True, required=False)
    emergency_contacts = EmergencyContactSerializer(many=True, required=False)
    educations = EducationSerializer(many=True, required=False)

    class Meta:
        model = Employee
        fields = "__all__"

    def update(self, instance, validated_data):
        work_histories = []
        emergency_contacts = []
        educations = []

        if validated_data.get("work_histories"):
            work_histories = validated_data.pop("work_histories")
        if validated_data.get("emergency_contacts"):
            emergency_contacts = validated_data.pop("emergency_contacts")
        if validated_data.get("educations"):
            educations = validated_data.pop("educations")

        user = super().update(instance, validated_data)

        if work_histories:
            for work in work_histories:
                work_history = WorkHistory.objects.create(**work)
                user.work_histories.add(work_history)

        if emergency_contacts:
            for contact in emergency_contacts:
                emergency_contact = EmergencyContact.objects.create(**contact)
                user.emergency_contacts.add(emergency_contact)

        if educations:
            for educ in educations:
                education = EmergencyContact.objects.create(**educ)
                user.educations.add(education)
        user.save()
        return user


