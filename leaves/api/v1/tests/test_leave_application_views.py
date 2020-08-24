from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from employees.tests.factories import EmployeeFactory
from leaves.tests.factories import (
    LeaveApplicationFactory,
    LeaveAllocationFactory,
    LeaveTypeFactory,
)
from leaves.models import LeaveApplication
from users.tests.factories import UserFactory


class LeaveApplicationTestCase(APITestCase):
    def setUp(self):
        self.employee = EmployeeFactory()
        self.user = self.employee.user
        self.approver1 = EmployeeFactory()
        self.approver2 = EmployeeFactory()
        self.leave_type = LeaveTypeFactory()
        self.leave_allocation = LeaveAllocationFactory(
            leave_type=self.leave_type, employee=self.employee
        )
        self.leave_application = LeaveApplicationFactory(
            employee=self.employee, leave_type=self.leave_type
        )
        self.leave_application.approvers.add(self.approver1, self.approver2)

    def test_leave_application_list_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("leaves-v1:leave-applications-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_leave_application_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("leaves-v1:leave-applications-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_leave_application(self):
        employee = EmployeeFactory()
        approver1 = EmployeeFactory()
        approver2 = EmployeeFactory()
        leave_type = LeaveTypeFactory()
        leave_allocation = LeaveAllocationFactory(
            employee=employee, leave_type=leave_type
        )
        data = {
            "approvers": {"add": [approver1.id, approver2.id]},
            "employee": employee.id,
            "leave_type": leave_type.id,
            "from_date": "2020-08-08",
            "to_date": "2020-08-15",
            "reason": "Vacation",
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("leaves-v1:leave-applications-list"), data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_leave_application_insufficient_allocation(self):
        employee = EmployeeFactory()
        approver1 = EmployeeFactory()
        approver2 = EmployeeFactory()
        leave_type1 = LeaveTypeFactory()
        leave_type2 = LeaveTypeFactory()
        leave_allocation = LeaveAllocationFactory(
            employee=employee, leave_type=leave_type1
        )
        data = {
            "approvers": {"add": [approver1.id, approver2.id]},
            "employee": employee.id,
            "leave_type": leave_type2.id,
            "from_date": "2020-08-08",
            "to_date": "2020-08-15",
            "reason": "Vacation",
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("leaves-v1:leave-applications-list"), data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_leave_application_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse(
                "leaves-v1:leave-applications-detail",
                kwargs={"pk": self.leave_application.id},
            )
        )
        self.assertTrue(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_leave_application_detail_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(
            reverse(
                "leaves-v1:leave-applications-detail",
                kwargs={"pk": self.leave_application.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_leave_application_by_approver(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("leaves-v1:leave-applications-list"),
            {"approvers": self.leave_application.approvers.first().user.first_name},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertIn(
            self.leave_application.approvers.first().user.first_name,
            response.data[0].get("approvers")[0].get("user").values(),
        )

    def test_search_leave_application_by_employee(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("leaves-v1:leave-applications-list"),
            {"employee": self.leave_application.employee.user.first_name},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertIn(
            self.leave_application.employee.user.first_name,
            response.data[0].get("employee").get("user").values(),
        )

    def test_search_leave_application_by_status(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("leaves-v1:leave-applications-list"), {"status": "draft"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertEqual("draft", response.data[0].get("status"))

    def test_search_leave_application_by_leave_type(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("leaves-v1:leave-applications-list"),
            {"leave_type": self.leave_type.id},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertEqual(
            self.leave_application.leave_type.id,
            response.data[0].get("leave_type").get("id"),
        )

    def test_patch_leave_application(self):
        leave_type = LeaveTypeFactory()
        leave_allocation = LeaveAllocationFactory(
            employee=self.employee, leave_type=leave_type
        )
        data = {"leave_type": leave_type.id}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse(
                "leaves-v1:leave-applications-detail",
                kwargs={"pk": self.leave_application.id},
            ),
            data=data,
            format="json",
        )
        self.leave_application.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.leave_application.leave_type, leave_type)

    def test_submit_leave_application(self):
        self.client.force_authenticate(user=self.user)
        leave_type = LeaveTypeFactory()
        leave_allocation = LeaveAllocationFactory(
            employee=self.employee, leave_type=leave_type
        )
        leave_application = LeaveApplicationFactory(
            leave_type=leave_type, employee=self.employee,
        )
        leave_application.approvers.add(self.approver1, self.approver2)
        response = self.client.post(
            reverse(
                "leaves-v1:leave-applications-submit",
                kwargs={"pk": leave_application.id},
            )
        )
        leave_application.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(leave_application.status, LeaveApplication.STATUS_SUBMITTED)

    def test_submit_leave_application_not_for_submission(self):
        self.client.force_authenticate(user=self.user)
        leave_type = LeaveTypeFactory()
        leave_allocation = LeaveAllocationFactory(
            employee=self.employee, leave_type=leave_type
        )
        leave_application = LeaveApplicationFactory(
            leave_type=leave_type,
            employee=self.employee,
            status=LeaveApplication.STATUS_CANCELLED,
        )
        leave_application.approvers.add(self.approver1, self.approver2)
        response = self.client.post(
            reverse(
                "leaves-v1:leave-applications-submit",
                kwargs={"pk": leave_application.id},
            )
        )
        leave_application.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(leave_application.status, LeaveApplication.STATUS_SUBMITTED)

    def test_approve_leave_application_invalid_approver(self):
        invalid_approver = EmployeeFactory(user=UserFactory())
        self.client.force_authenticate(user=invalid_approver.user)
        response = self.client.post(
            reverse(
                "leaves-v1:leave-applications-approve",
                kwargs={"pk": self.leave_application.id},
            )
        )
        self.leave_application.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(
            self.leave_application.status, LeaveApplication.STATUS_APPROVED
        )

    def test_approve_leave_application(self):
        self.client.force_authenticate(user=self.approver1.user)
        leave_type = LeaveTypeFactory()
        leave_allocation = LeaveAllocationFactory(
            employee=self.employee, leave_type=leave_type
        )
        leave_application = LeaveApplicationFactory(
            leave_type=leave_type,
            employee=self.employee,
            status=LeaveApplication.STATUS_SUBMITTED,
        )
        leave_application.approvers.add(self.approver1, self.approver2)
        response = self.client.post(
            reverse(
                "leaves-v1:leave-applications-approve",
                kwargs={"pk": leave_application.id},
            )
        )
        leave_application.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(leave_application.status, LeaveApplication.STATUS_APPROVED)

    def test_approve_leave_application_not_for_approval(self):
        self.client.force_authenticate(user=self.approver1.user)
        leave_type = LeaveTypeFactory()
        leave_allocation = LeaveAllocationFactory(
            employee=self.employee, leave_type=leave_type
        )
        leave_application = LeaveApplicationFactory(
            leave_type=leave_type, employee=self.employee,
        )
        leave_application.approvers.add(self.approver1, self.approver2)
        response = self.client.post(
            reverse(
                "leaves-v1:leave-applications-approve",
                kwargs={"pk": leave_application.id},
            )
        )
        leave_application.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(leave_application.status, LeaveApplication.STATUS_APPROVED)

    def test_decline_leave_application_invalid_approver(self):
        invalid_approver = EmployeeFactory(user=UserFactory())
        self.client.force_authenticate(user=invalid_approver.user)
        response = self.client.post(
            reverse(
                "leaves-v1:leave-applications-decline",
                kwargs={"pk": self.leave_application.id},
            )
        )
        self.leave_application.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(
            self.leave_application.status, LeaveApplication.STATUS_DECLINED
        )

    def test_decline_leave_application(self):
        self.client.force_authenticate(user=self.approver1.user)
        leave_type = LeaveTypeFactory()
        leave_allocation = LeaveAllocationFactory(
            employee=self.employee, leave_type=leave_type
        )
        leave_application = LeaveApplicationFactory(
            leave_type=leave_type,
            employee=self.employee,
            status=LeaveApplication.STATUS_SUBMITTED,
        )
        leave_application.approvers.add(self.approver1, self.approver2)
        response = self.client.post(
            reverse(
                "leaves-v1:leave-applications-decline",
                kwargs={"pk": leave_application.id},
            )
        )
        leave_application.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(leave_application.status, LeaveApplication.STATUS_DECLINED)

    def test_decline_leave_application_not_for_decline(self):
        self.client.force_authenticate(user=self.approver1.user)
        leave_type = LeaveTypeFactory()
        leave_allocation = LeaveAllocationFactory(
            employee=self.employee, leave_type=leave_type
        )
        leave_application = LeaveApplicationFactory(
            leave_type=leave_type,
            employee=self.employee,
            status=LeaveApplication.STATUS_APPROVED,
        )
        leave_application.approvers.add(self.approver1, self.approver2)
        response = self.client.post(
            reverse(
                "leaves-v1:leave-applications-decline",
                kwargs={"pk": leave_application.id},
            )
        )
        leave_application.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(leave_application.status, LeaveApplication.STATUS_DECLINED)

    def test_cancel_leave_application(self):
        self.client.force_authenticate(user=self.user)
        leave_type = LeaveTypeFactory()
        leave_allocation = LeaveAllocationFactory(
            employee=self.employee, leave_type=leave_type
        )
        leave_application = LeaveApplicationFactory(
            leave_type=leave_type,
            employee=self.employee,
            status=LeaveApplication.STATUS_SUBMITTED,
        )
        leave_application.approvers.add(self.approver1, self.approver2)
        response = self.client.post(
            reverse(
                "leaves-v1:leave-applications-cancel",
                kwargs={"pk": leave_application.id},
            )
        )
        leave_application.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(leave_application.status, LeaveApplication.STATUS_CANCELLED)

    def test_cancel_leave_application_not_for_cancellation(self):
        self.client.force_authenticate(user=self.user)
        leave_type = LeaveTypeFactory()
        leave_allocation = LeaveAllocationFactory(
            employee=self.employee, leave_type=leave_type
        )
        leave_application = LeaveApplicationFactory(
            leave_type=leave_type,
            employee=self.employee,
            status=LeaveApplication.STATUS_APPROVED,
        )
        leave_application.approvers.add(self.approver1, self.approver2)
        response = self.client.post(
            reverse(
                "leaves-v1:leave-applications-cancel",
                kwargs={"pk": leave_application.id},
            )
        )
        leave_application.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(leave_application.status, LeaveApplication.STATUS_CANCELLED)

