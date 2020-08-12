import json

from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate

from django.urls import reverse

from leaves.api.v1.serializers import LeaveTypeSerializer
from leaves.tests.factories import LeaveTypeFactory
from users.tests.factories import UserFactory


class LeaveTypeSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.leave_type = LeaveTypeFactory()

        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("leave-types-list"))
        self.response_data = json.loads(response.content)

    def test_leave_type_object(self):
        leave_type_serializer_data = LeaveTypeSerializer(self.leave_type).data
        leave_type_serializer_data = [leave_type_serializer_data]
        self.assertEqual(self.response_data, leave_type_serializer_data)
