from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from core.models import OPTIONAL


class User(AbstractUser):
    middle_name = models.CharField("Middle Name", max_length=150, null=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.get_full_name()


class Employee(models.Model):

    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    user = models.OneToOneField(
        "users.User",
        verbose_name="User",
        related_name="employee",
        on_delete=models.CASCADE,
    )

    gender = models.CharField("Gender", choices=GENDER_CHOICES, max_length=50,)
    date_of_birth = models.DateField("Date of Birth", auto_now_add=False,)
    date_started = models.DateField("Date Started", auto_now_add=False,)
    is_active = models.BooleanField("Is active", default=True,)
    nickname = models.CharField("Nickname", max_length=100, **OPTIONAL,)

    def __str__(self):
        return self.user.get_full_name()


class EmergencyContact(models.Model):

    name = models.CharField("Name", max_length=100,)
    contact_number = models.CharField("Contact No.", max_length=100,)
    employee = models.ForeignKey(
        "users.employee",
        verbose_name="Employee",
        related_name="emergency_contact",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Emercency Contact")
        verbose_name_plural = _("Emergency Contacts")

    def __str__(self):
        return self.name


class Education(models.Model):
    school = models.CharField("School", max_length=100,)
    level = models.CharField("Level", max_length=100,)
    degree = models.CharField("Degree", max_length=100,)
    year_graduated = models.CharField("Year Graduated", max_length=50,)

    employee = models.ForeignKey(
        "users.employee",
        verbose_name="Employee",
        related_name="education",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.school

    class Meta:
        verbose_name = _("Education")
        verbose_name_plural = _("Education")


class WorkHistory(models.Model):
    company = models.CharField("Company", max_length=100,)
    position = models.CharField("Position", max_length=100,)
    employee = models.ForeignKey(
        "users.employee",
        verbose_name="Employee",
        related_name="work_history",
        on_delete=models.CASCADE,
        **OPTIONAL,
    )

    def __str__(self):
        return self.position

    class Meta:
        verbose_name = _("Work History")
        verbose_name_plural = _("Work History")
