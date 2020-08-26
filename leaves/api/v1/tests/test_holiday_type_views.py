from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from leaves.models import HolidayType
from leaves.tests.factories import HolidayTypeFactory
from users.tests.factories import UserFactory


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
        holiday_type_amount = HolidayType.objects.count()
        response = self.client.delete(
            reverse(
                "leaves-v1:holiday-types-detail", kwargs={"pk": self.holiday_type.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(holiday_type_amount, 0)
