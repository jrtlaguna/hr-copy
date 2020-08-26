from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse
from django.utils import timezone

from leaves.tests.factories import HolidayFactory, HolidayTypeFactory
from users.tests.factories import UserFactory


class HolidayTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True)
        self.holiday_type = HolidayTypeFactory()
        self.holiday = HolidayFactory(holiday_type=self.holiday_type)

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
            "holiday_type": self.holiday_type.id,
            "name": "Test holiday 1",
            "date": timezone.now().date(),
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("leaves-v1:holidays-list"), data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_holiday_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("leaves-v1:holidays-detail", kwargs={"pk": self.holiday.id},)
        )
        self.assertTrue(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_holiday_by_holiday_type(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("leaves-v1:holidays-list"),
            {"holiday_type": self.holiday.holiday_type.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertEqual(
            self.holiday.holiday_type.id, response.data[0].get("holiday_type"),
        )

    def test_holiday_invalid_date(self):
        data = {
            "holiday_type": self.holiday_type.id,
            "name": "Test holiday 1",
            "date": "2020-8-25",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("leaves-v1:holidays-list"), data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

    def test_archive_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(
            reverse("leaves-v1:holidays-detail", kwargs={"pk": self.holiday.id},)
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_archive_holiday(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse("leaves-v1:holidays-detail", kwargs={"pk": self.holiday.id},)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
