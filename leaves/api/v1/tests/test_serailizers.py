import json

from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from django.urls import reverse

from employees.tests.factories import EmployeeFactory
from leaves.api.v1.serializers import LeaveAllocationSerializer, LeaveTypeSerializer
from leaves.tests.factories import (
    HolidayFactory,
    HolidayTypeFactory,
    LeaveAllocationFactory,
    LeaveTypeFactory,
)
from users.tests.factories import UserFactory


class LeaveTypeSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True)
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
        self.user = UserFactory(is_staff=True)
        self.employee = EmployeeFactory()
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


class HolidaySerializerTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True)
        self.type = HolidayTypeFactory()
        self.holiday = HolidayFactory(type=self.type)

    def test_holiday_invalid_date(self):
        data = {
            "type": self.type.id,
            "name": "Test holiday 1",
            "date": "2020-8-25",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("leaves-v1:holidays-list"), data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
