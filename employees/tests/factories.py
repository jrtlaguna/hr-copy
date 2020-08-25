import factory

from employees.models import Education, EmergencyContact, Employee, WorkHistory
from users.tests.factories import UserFactory


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    user = factory.SubFactory(UserFactory)
    date_of_birth = "1994-01-01"
    contact_number = "09224567895"
    address = "PH"
    date_started = "2020-07-07"
    nickname = "roger"


class EducationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Education

    employee = factory.SubFactory(EmployeeFactory)
    school = "ABC University"
    level = "Tertiary"
    degree = "BSIT"
    year_graduated = "2015"


class EmergencyContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmergencyContact

    employee = factory.SubFactory(EmployeeFactory)
    name = "Foo"
    contact_number = "09121239999"
    relation = "Father"


class WorkHistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WorkHistory

    employee = factory.SubFactory(EmployeeFactory)
    company = "Company A"
    position = "Software Developer"
    date_started = "2018-07-07"
    date_ended = "2020-06-08"
