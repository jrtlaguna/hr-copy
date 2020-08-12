from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate

from django.urls import reverse

from leaves.tests.factories import LeaveTypeFactory
from users.tests.factories import UserFactory


class LeaveTypeTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.leave_type = LeaveTypeFactory()

    def test_leave_type_list_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("leaves-v1:leave-types-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_leave_type_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("leaves-v1:leave-types-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_leave_type(self):
        data = {
            "name": "Sick Leave",
            "is_paid": True,
            "is_optional": True,
            "is_convertible_to_cash": True,
            "is_carry_forwarded": False,
            "is_active": True,
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("leaves-v1:leave-types-list"), data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_leave_type_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("leaves-v1:leave-types-detail", kwargs={"pk": self.leave_type.id})
        )
        self.assertTrue(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_leave_type_by_name(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("leaves-v1:leave-types-list"), {"search": "unpaid"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertIn("unpaid", response.data[0].get("name").lower())

    def test_update_leave_type_unauthorized(self):
        data = {"name": "Maternity Leave"}
        self.client.force_authenticate(user=None)
        response = self.client.patch(
            reverse("leaves-v1:leave-types-detail", kwargs={"pk": self.leave_type.id}),
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_leave_type(self):
        data = {
            "name": "Paternity Leave",
            "is_paid": False,
            "is_optional": False,
            "is_convertible_to_cash": False,
            "is_carry_forwarded": False,
            "is_active": True,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            reverse("leaves-v1:leave-types-detail", kwargs={"pk": self.leave_type.id}),
            data=data,
            format="json",
        )
        self.leave_type.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), "Paternity Leave")
        self.assertEqual(response.data.get("is_paid"), False)

    def test_patch_leave_type(self):
        data = {
            "is_carry_forwarded": True,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse("leaves-v1:leave-types-detail", kwargs={"pk": self.leave_type.id}),
            data=data,
            format="json",
        )
        self.leave_type.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("is_carry_forwarded"), True)

    def test_archive_employee(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse("leaves-v1:leave-types-detail", kwargs={"pk": self.leave_type.id})
        )
        self.leave_type.refresh_from_db()
        self.assertEqual(self.leave_type.is_active, False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
