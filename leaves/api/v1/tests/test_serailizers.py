import json

from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from django.urls import reverse

from employees.tests.factories import EmployeeFactory
from leaves.api.v1.serializers import LeaveAllocationSerializer, LeaveTypeSerializer
from leaves.tests.factories import LeaveAllocationFactory, LeaveTypeFactory
from users.tests.factories import UserFactory


class LeaveTypeSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.leave_type = LeaveTypeFactory()

        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("leaves-v1:leave-types-list"))
        self.response_data = json.loads(response.content)

    def test_leave_type_object(self):
        leave_type_serializer_data = LeaveTypeSerializer(self.leave_type).data
        leave_type_serializer_data = [leave_type_serializer_data]
        self.assertEqual(self.response_data, leave_type_serializer_data)


class LeaveAllocationSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.employee = EmployeeFactory(user=self.user)
        self.leave_type = LeaveTypeFactory()
        self.leave_allocation = LeaveAllocationFactory(
            employee=self.employee, leave_type=self.leave_type
        )

        factory = APIRequestFactory()
        request = factory.get("/")
        self.serializer_context = {"request": Request(request)}

        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("leaves-v1:leave-allocations-list"))
        self.response_data = json.loads(response.content)

    def test_leave_allocation_object(self):
        leave_allocation_serializer_data = LeaveAllocationSerializer(
            self.leave_allocation, context=self.serializer_context
        ).data
        leave_allocation_serializer_data = [leave_allocation_serializer_data]
        self.assertEqual(self.response_data, leave_allocation_serializer_data)
