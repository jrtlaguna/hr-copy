from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APIRequestFactory,
    APITestCase,
    APITransactionTestCase,
    force_authenticate,
)

from employees.models import Employee


class EmployeeViewsetTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(
            password="testuserpassword",
            first_name="Foo",
            last_name="Bar",
            email="testuser@gmail.com",
        )
        self.employee = Employee.objects.create(
            user=self.user,
            date_of_birth="1994-01-01",
            contact_number="09224567895",
            address="PH",
            date_started="2020-07-07",
            nickname="roger",
        )

    def test_employee_list_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("employees-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_employee_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("employees-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_employee(self):
        data = {
            "user": {
                "first_name": "Foo",
                "last_name": "Bar",
                "email": "foobar@gmail.com",
            },
            "work_histories": [
                {
                    "company": "Company A",
                    "position": "Software Developer",
                    "date_started": "2020-02-28",
                    "date_ended": "2020-07-15",
                }
            ],
            "emergency_contacts": [
                {
                    "name": "Foo Bar Sr",
                    "contact_number": "+639021237654",
                    "relation": "Father",
                }
            ],
            "educations": [
                {
                    "school": "ABC University",
                    "level": "Tertiary",
                    "degree": "BS in Computer Science",
                    "year_graduated": "2015",
                }
            ],
            "gender": "male",
            "date_of_birth": "1994-01-01",
            "contact_number": "09224567895",
            "address": "PH",
            "date_started": "2020-07-07",
            "nickname": "roger",
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("employees-list"), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_employee_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("employees-detail", kwargs={"pk": self.employee.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_by_nickname(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("employees-list"), {"search": "roger"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(bool(response.json()))
        self.assertIn("roger", response.json()[0].get("nickname"))

    def test_search_by_firstname(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("employees-list"), {"search": "foo"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(bool(response.json()))
        self.assertIn("foo", response.json()[0]["user"].get("first_name").lower())

    def test_search_by_lastname(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("employees-list"), {"search": "bar"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(bool(response.json()))
        self.assertIn("bar", response.json()[0]["user"].get("last_name").lower())

    def test_search_by_email(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("employees-list"), {"search": "testuser"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(bool(response.json()))
        self.assertIn("testuser", response.json()[0]["user"].get("email"))

    def test_update_employee_unauthorized(self):
        data = {"user": {"email": "newemail@gmail.com"}}
        self.client.force_authenticate(user=None)
        response = self.client.patch(
            reverse("employees-detail", kwargs={"pk": self.employee.id}),
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_employee(self):
        data = {
            "user": {
                "first_name": "Foo",
                "middle_name": "K",
                "last_name": "Bar",
                "email": "foobar@gmail.com",
            },
            "work_histories": [
                {
                    "company": "Company A",
                    "position": "Software Developer",
                    "date_started": "2020-02-28",
                    "date_ended": "2020-07-15",
                }
            ],
            "emergency_contacts": [
                {
                    "name": "Foo Bar Sr",
                    "contact_number": "+639021237654",
                    "relation": "Father",
                }
            ],
            "educations": [
                {
                    "school": "ABC University",
                    "level": "Tertiary",
                    "degree": "BS in Computer Science",
                    "year_graduated": "2015",
                }
            ],
            "gender": "male",
            "date_of_birth": "1994-01-01",
            "contact_number": "09224567895",
            "address": "PH",
            "date_started": "2020-07-07",
            "nickname": "bartolomefoo",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            reverse("employees-detail", kwargs={"pk": self.employee.id}),
            data=data,
            format="json",
        )
        self.employee.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.employee.nickname, "bartolomefoo")
        self.assertEqual(self.employee.user.middle_name, "K")

    def test_patch_employee(self):
        data = {"user": {"email": "newemail@gmail.com"}}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse("employees-detail", kwargs={"pk": self.employee.id}),
            data=data,
            format="json",
        )
        self.employee.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.employee.user.email, "newemail@gmail.com")

    def test_archive_employee_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.patch(
            reverse("employees-detail", kwargs={"pk": self.employee.id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_archive_employee(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse("employees-detail", kwargs={"pk": self.employee.id})
        )
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.user.is_active, False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

