import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from employees.models import Education, EmergencyContact, Employee, WorkHistory

from .serializers import (
    EducationSerializer,
    EmergencyContactSerializer,
    EmployeeSerializer,
    UserSerializer,
    WorkHistorySerializer,
)


class EmployeeSerializerTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(
            password="testuserpassword",
            first_name="Foo",
            last_name="Bar",
            email="testuser@gmail.com",
        )

        self.employee = Employee.objects.create(
            user=self.user,
            date_of_birth="1994-01-01",
            contact_number="09224567895",
            address="PH",
            date_started="2020-07-07",
            nickname="roger",
        )

        education = Education.objects.create(
            employee=self.employee,
            school="ABC University",
            level="Tertiary",
            degree="BSIT",
            year_graduated="2015",
        )

        emergency_contact = EmergencyContact.objects.create(
            name="Foo",
            contact_number="09121239999",
            relation="Father",
            employee=self.employee,
        )

        work_history = WorkHistory.objects.create(
            company="Company A",
            position="Software Developer",
            date_started="2018-07-07",
            date_ended="2020-06-08",
            employee=self.employee,
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("employees-list"))
        self.response_data = json.loads(response.content)

    def test_employee_object(self):
        employee_serializer_data = json.dumps(EmployeeSerializer(self.employee).data)
        employee_serializer_data = [json.loads(employee_serializer_data)]
        self.assertEqual(self.response_data, employee_serializer_data)

    def test_employee_user_object(self):
        user = self.employee.user
        user_serializer_data = json.dumps(UserSerializer(user).data)
        user_serializer_data = json.loads(user_serializer_data)
        user_response_data = self.response_data[0].get("user")
        self.assertEqual(user_response_data, user_serializer_data)

    def test_employee_education_object(self):
        educations = self.employee.educations.all()
        education_serializer_data = json.dumps(
            EducationSerializer(educations, many=True).data
        )
        education_serializer_data = json.loads(education_serializer_data)
        education_response_data = self.response_data[0].get("educations")
        self.assertEqual(education_response_data, education_serializer_data)

    def test_employee_emergency_contact_object(self):
        emergency_contacts = self.employee.emergency_contacts.all()
        emergency_contact_serializer_data = json.dumps(
            EmergencyContactSerializer(emergency_contacts, many=True).data
        )
        emergency_contact_serializer_data = json.loads(
            emergency_contact_serializer_data
        )
        emergency_contacts_response_data = self.response_data[0].get(
            "emergency_contacts"
        )
        self.assertEqual(
            emergency_contacts_response_data, emergency_contact_serializer_data
        )

    def test_employee_work_history_object(self):
        work_histories = self.employee.work_histories.all()
        work_history_serializer_data = json.dumps(
            WorkHistorySerializer(work_histories, many=True).data
        )
        work_history_serializer_data = json.loads(work_history_serializer_data)
        work_history_response_data = self.response_data[0].get("work_histories")
        self.assertEqual(work_history_response_data, work_history_serializer_data)
