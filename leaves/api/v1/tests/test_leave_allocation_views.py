from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate

from django.urls import reverse

from employees.tests.factories import EmployeeFactory
from leaves.tests.factories import LeaveAllocationFactory, LeaveTypeFactory
from users.tests.factories import UserFactory


class LeaveAllocationTestCase(APITestCase):
    def setUp(self):
        self.leave_allocation = LeaveAllocationFactory()
        self.leave_type = LeaveTypeFactory()
        self.employee = self.leave_allocation.employee
        self.user = self.employee.user

    def test_get_leave_allocation_list_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("leaves-v1:leave-allocations-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_leave_allocation_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("leaves-v1:leave-allocations-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_leave_allocation(self):
        data = {
            "leave_type": self.leave_type.id,
            "employee": self.employee.id,
            "from_date": "2020-01-01",
            "to_date": "2020-12-12",
            "count": 5,
            "notes": "Test Leave Allocation",
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("leaves-v1:leave-allocations-list"), data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_leave_allocation_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse(
                "leaves-v1:leave-allocations-detail",
                kwargs={"pk": self.leave_allocation.id},
            )
        )
        self.assertTrue(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_leave_allocation_by_leave_type(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("leaves-v1:leave-allocations-list"), {"leave_type": "unpaid"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertIn("unpaid", response.data[0].get("leave_type").get("name").lower())

    def test_search_leave_allocation_by_is_active(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("leaves-v1:leave-allocations-list"), {"is_active": True}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertTrue(True, response.data[0].get("is_active"))

    def test_search_leave_allocation_by_employee_name(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("leaves-v1:leave-allocations-list"), {"name": "Foo"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertIn("Foo", response.data[0].get("employee").values())

    def test_patch_leave_allocation_unauthorized(self):
        data = {"count": 3}
        self.client.force_authenticate(user=None)
        response = self.client.patch(
            reverse(
                "leaves-v1:leave-allocations-detail",
                kwargs={"pk": self.leave_allocation.id},
            ),
            data=data,
            format="json",
        )
        self.leave_allocation.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_leave_allocation(self):
        data = {"count": 2}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse(
                "leaves-v1:leave-allocations-detail",
                kwargs={"pk": self.leave_allocation.id},
            ),
            data=data,
            format="json",
        )
        self.leave_allocation.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.leave_allocation.count, 2)

    def test_archive_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(
            reverse(
                "leaves-v1:leave-allocations-detail",
                kwargs={"pk": self.leave_allocation.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_archive_leave_allocation(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse(
                "leaves-v1:leave-allocations-detail",
                kwargs={"pk": self.leave_allocation.id},
            )
        )
        self.leave_allocation.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.leave_allocation.is_active, False)
