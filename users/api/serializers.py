from rest_framework import serializers

from users.models import (
    Employee,
    User,
    EmergencyContact,
    WorkHistory,
    Education
)


class EmployeeSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    middle_name = serializers.CharField(source='user.middle_name')
    last_name = serializers.CharField(source='user.last_name')


    class Meta:
        model = Employee
        exclude = [
            'id',
            'user',
        ]

    # def validate_email(self, email):

class EmergencyContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmergencyContact
        exclude = ['id',]

class WorkHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkHistory
        exclude = ['id',]

class EducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Education
        exclude = ['id',]