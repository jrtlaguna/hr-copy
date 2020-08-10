import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from employees.models import Education, EmergencyContact, Employee, WorkHistory
from employees.api.v1.serializers import (
    EducationSerializer,
    EmergencyContactSerializer,
    EmployeeSerializer,
    UserSerializer,
    WorkHistorySerializer,
)
from employees.tests.factories import *


class EmployeeSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.employee = EmployeeFactory(user=self.user)
        education = EducationFactory(employee=self.employee)
        emergency_contact = EmergencyContact(employee=self.employee)
        work_history = WorkHistoryFactory(employee=self.employee)

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
