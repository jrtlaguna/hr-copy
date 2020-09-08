from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse
from django.utils import timezone

from employees.tests.factories import EmployeeFactory
from leaves.models import (
    Holiday,
    HolidayType,
    LeaveApplication,
)
from leaves.tests.factories import (
    HolidayFactory,
    HolidayTypeFactory,
    LeaveAllocationFactory,
    LeaveApplicationFactory,
    LeaveTypeFactory,
)
from users.tests.factories import UserFactory


class HolidayTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True)
        self.type = HolidayTypeFactory()
        self.holiday = HolidayFactory(type=self.type)

    def test_get_holiday_list_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("leaves-v1:holidays-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_holiday_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("leaves-v1:holidays-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_holiday(self):
        data = {
            "type": self.type.id,
            "name": "Test holiday 1",
            "date": timezone.now().date(),
        }

        self.client.force_authenticate(user=self.user)
        holiday_count = Holiday.objects.count()
        response = self.client.post(
            reverse("leaves-v1:holidays-list"), data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(holiday_count + 1, Holiday.objects.count())

    def test_get_holiday_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("leaves-v1:holidays-detail", kwargs={"pk": self.holiday.id},)
        )
        self.assertTrue(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_holiday_by_type(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("leaves-v1:holidays-list"), {"type": self.holiday.type.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertEqual(
            self.holiday.type.id, response.data[0].get("type").get("id"),
        )

    def test_patch_holiday_unauthorized(self):
        data = {"name": "New Name"}
        self.client.force_authenticate(user=None)
        response = self.client.patch(
            reverse("leaves-v1:holidays-detail", kwargs={"pk": self.holiday.id},),
            data=data,
            format="json",
        )
        self.holiday.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(self.holiday.name, "New Name")

    def test_patch_holiday(self):
        data = {"name": "New Name"}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse("leaves-v1:holidays-detail", kwargs={"pk": self.holiday.id},),
            data=data,
            format="json",
        )
        self.holiday.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.holiday.name, "New Name")

    def test_delete_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(
            reverse("leaves-v1:holidays-detail", kwargs={"pk": self.holiday.id},)
        )
        holiday_count = Holiday.objects.count()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(holiday_count, 1)

    def test_delete_holiday(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse("leaves-v1:holidays-detail", kwargs={"pk": self.holiday.id},)
        )
        holiday_count = Holiday.objects.count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(holiday_count, 0)


class HolidayTypeTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True)
        self.holiday_type = HolidayTypeFactory()

    def test_holiday_type_list_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("leaves-v1:holiday-types-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_holiday_type_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("leaves-v1:holiday-types-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_holiday_type(self):
        data = {
            "name": "Test Name",
            "is_no_work_no_pay": True,
            "pay_percentage": 0.3,
        }

        self.client.force_authenticate(user=self.user)
        holiday_type_count = HolidayType.objects.count()
        response = self.client.post(
            reverse("leaves-v1:holiday-types-list"), data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(holiday_type_count + 1, HolidayType.objects.count())

    def test_get_holiday_type_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse(
                "leaves-v1:holiday-types-detail", kwargs={"pk": self.holiday_type.id}
            )
        )
        self.assertTrue(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_holiday_type_unauthorized(self):
        data = {"pay_percentage": 0.7}
        self.client.force_authenticate(user=None)
        response = self.client.patch(
            reverse(
                "leaves-v1:holiday-types-detail", kwargs={"pk": self.holiday_type.id}
            ),
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(self.holiday_type.pay_percentage, 0.7)

    def test_put_holiday_type(self):
        data = {
            "name": "Test Name",
            "is_no_work_no_pay": False,
            "pay_percentage": 0.7,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            reverse(
                "leaves-v1:holiday-types-detail", kwargs={"pk": self.holiday_type.id}
            ),
            data=data,
            format="json",
        )
        self.holiday_type.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("pay_percentage"), 0.7)
        self.assertFalse(response.data.get("is_no_work_no_pay"))

    def test_patch_holiday_type(self):
        data = {
            "is_no_work_no_pay": False,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse(
                "leaves-v1:holiday-types-detail", kwargs={"pk": self.holiday_type.id}
            ),
            data=data,
            format="json",
        )
        self.holiday_type.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data.get("is_no_work_no_pay"))

    def test_delete_holiday_type(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse(
                "leaves-v1:holiday-types-detail", kwargs={"pk": self.holiday_type.id}
            )
        )
        holiday_type_count = HolidayType.objects.count()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(holiday_type_count, 0)


class LeaveAllocationTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True)
        self.employee = EmployeeFactory()
        self.leave_type = LeaveTypeFactory()
        self.leave_allocation = LeaveAllocationFactory(
            employee=self.employee, leave_type=self.leave_type
        )

    def test_get_leave_allocation_list_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("leaves-v1:leave-allocations-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_leave_allocation_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("leaves-v1:leave-allocations-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_leave_allocation(self):
        leave_type = LeaveTypeFactory()
        data = {
            "leave_type": leave_type.id,
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
            reverse("leaves-v1:leave-allocations-list"),
            {"leave_type": self.leave_allocation.leave_type.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertEqual(
            self.leave_allocation.leave_type.id,
            response.data[0].get("leave_type").get("id"),
        )

    def test_search_leave_allocation_by_is_active(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("leaves-v1:leave-allocations-list"), {"is_active": True}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertTrue(True, response.data[0].get("is_active"))

    def test_search_leave_allocation_by_employee(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("leaves-v1:leave-allocations-list"),
            {"employee": self.employee.nickname},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertIn(
            self.employee.nickname, response.data[0].get("employee").values(),
        )

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
            "from_date": timezone.now().date(),
            "to_date": timezone.now().date() + timedelta(3),
            "reason": "Vacation",
        }
        number_of_leave_days = Holiday.business_days_count(data.get("from_date"), data.get("to_date"))
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("leaves-v1:leave-applications-list"), data=data, format="json"
        )
        self.assertEqual(number_of_leave_days, response.data.get("count"))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_leave_application_insufficient_allocation(self):
        employee = EmployeeFactory()
        approver1 = EmployeeFactory()
        approver2 = EmployeeFactory()
        leave_type1 = LeaveTypeFactory()
        leave_type2 = LeaveTypeFactory()
        leave_allocation1 = LeaveAllocationFactory(
            employee=employee, leave_type=leave_type1
        )
        leave_allocation2 = LeaveAllocationFactory(
            employee=employee, leave_type=leave_type2, count=1
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

    def test_put_leave_application(self):
        new_leave_type = LeaveTypeFactory()
        leave_allocation = LeaveAllocationFactory(
            employee=self.employee, leave_type=new_leave_type
        )
        data = {
            "approvers": {},
            "employee": self.leave_application.employee.id,
            "leave_type": new_leave_type.id,
            "from_date": "2020-08-12",
            "to_date": "2020-08-15",
            "reason": "Out of town.",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            reverse(
                "leaves-v1:leave-applications-detail",
                kwargs={"pk": self.leave_application.id},
            ),
            data=data,
            format="json",
        )
        self.leave_application.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.leave_application.leave_type, new_leave_type)
        self.assertEqual(self.leave_application.reason, data.get("reason"))
        self.assertEqual(
            self.leave_application.from_date,
            datetime.strptime(data.get("from_date"), "%Y-%m-%d").date(),
        )

    def test_patch_leave_application(self):
        leave_type = LeaveTypeFactory()
        leave_allocation = LeaveAllocationFactory(
            employee=self.employee, leave_type=leave_type
        )
        data = {
            "leave_type": leave_type.id,
            "to_date":  timezone.now().date() + timedelta(4)
        }
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
        number_of_leave_days = Holiday.business_days_count(self.leave_application.from_date, self.leave_application.to_date)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.leave_application.leave_type, leave_type)
        self.assertEqual(self.leave_application.count, number_of_leave_days)

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
        holiday_type = HolidayTypeFactory()
        holidays = HolidayFactory(date="2020-08-31", type=holiday_type)
        leave_type = LeaveTypeFactory()
        leave_allocation = LeaveAllocationFactory(
            employee=self.employee, leave_type=leave_type
        )
        leave_application = LeaveApplicationFactory(
            leave_type=leave_type,
            employee=self.employee,
            status=LeaveApplication.STATUS_SUBMITTED
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


class LeaveTypeTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True)
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

    def test_archive_leave_type(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse("leaves-v1:leave-types-detail", kwargs={"pk": self.leave_type.id})
        )
        self.leave_type.refresh_from_db()
        self.assertEqual(self.leave_type.is_active, False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
