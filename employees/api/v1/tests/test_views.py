from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from employees.tests.factories import EmployeeFactory
from users.tests.factories import UserFactory


class EmployeeViewsetTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.employee = EmployeeFactory(user=self.user)

    def test_employee_list_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("employees-v1:employees-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_employee_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("employees-v1:employees-list"))
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
        response = self.client.post(
            reverse("employees-v1:employees-list"), data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_employee_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("employees-v1:employees-detail", kwargs={"pk": self.employee.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_by_nickname(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("employees-v1:employees-list"), {"search": "roger"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(bool(response.json()))
        self.assertIn("roger", response.json()[0].get("nickname"))

    def test_search_by_firstname(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("employees-v1:employees-list"), {"search": "foo"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(bool(response.json()))
        self.assertIn("foo", response.json()[0]["user"].get("first_name").lower())

    def test_search_by_lastname(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("employees-v1:employees-list"), {"search": "bar"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(bool(response.json()))
        self.assertIn("bar", response.json()[0]["user"].get("last_name").lower())

    def test_search_by_email(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("employees-v1:employees-list"), {"search": self.employee.user.email}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(bool(response.json()))
        self.assertIn(self.employee.user.email, response.json()[0]["user"].get("email"))

    def test_update_employee_unauthorized(self):
        data = {"user": {"email": "newemail@gmail.com"}}
        self.client.force_authenticate(user=None)
        response = self.client.patch(
            reverse("employees-v1:employees-detail", kwargs={"pk": self.employee.id}),
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
            reverse("employees-v1:employees-detail", kwargs={"pk": self.employee.id}),
            data=data,
            format="json",
        )
        self.employee.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.employee.user.id, self.user.id)
        self.assertEqual(self.employee.nickname, "bartolomefoo")
        self.assertEqual(self.employee.user.middle_name, "K")

    def test_patch_employee(self):
        data = {"user": {"email": "newemail@gmail.com"}}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse("employees-v1:employees-detail", kwargs={"pk": self.employee.id}),
            data=data,
            format="json",
        )
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.user.id, self.user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.employee.user.email, "newemail@gmail.com")

    def test_archive_employee_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.patch(
            reverse("employees-v1:employees-detail", kwargs={"pk": self.employee.id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_archive_employee(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse("employees-v1:employees-detail", kwargs={"pk": self.employee.id})
        )
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.user.is_active, False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

