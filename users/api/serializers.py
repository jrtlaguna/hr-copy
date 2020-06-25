from rest_framework import serializers

from users.models import (
    Employee,
    User,
    EmergencyContact,
    WorkHistory,
    Education,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "middle_name",
            "last_name",
            "username",
            "email",
        )


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


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    work_history = WorkHistorySerializer(many=True,)
    emergency_contact = EmergencyContactSerializer(many=True,)
    education = EducationSerializer(many=True,)

    class Meta:
        model = Employee
        fields = "__all__"
