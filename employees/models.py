from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import OPTIONAL


class Employee(models.Model):

    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    user = models.OneToOneField(
        "users.User",
        verbose_name=_("User"),
        related_name="employee",
        on_delete=models.CASCADE,
    )

    gender = models.CharField(_("Gender"), choices=GENDER_CHOICES, max_length=50,)
    date_of_birth = models.DateField(_("Date of Birth"), **OPTIONAL,)
    date_started = models.DateField(_("Date Started"), **OPTIONAL,)
    is_active = models.BooleanField(_("Is active"), default=True,)
    nickname = models.CharField(_("Nickname"), max_length=100, **OPTIONAL,)

    def __str__(self):
        return self.user.get_full_name()


class EmergencyContact(models.Model):

    name = models.CharField(_("Name"), max_length=100,)
    contact_number = models.CharField(_("Contact No."), max_length=100,)
    employee = models.ForeignKey(
        "employees.employee",
        verbose_name=_("Employee"),
        related_name="emergency_contacts",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Emercency Contact")
        verbose_name_plural = _("Emergency Contacts")

    def __str__(self):
        return self.name


class Education(models.Model):
    school = models.CharField(_("School"), max_length=100,)
    level = models.CharField(_("Level"), max_length=100,)
    degree = models.CharField(_("Degree"), max_length=100,)
    year_graduated = models.CharField(_("Year Graduated"), max_length=50,)

    employee = models.ForeignKey(
        "employees.employee",
        verbose_name=_("Employee"),
        related_name="educations",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.school

    class Meta:
        verbose_name = _("Education")
        verbose_name_plural = _("Education")


class WorkHistory(models.Model):
    company = models.CharField(_("Company"), max_length=100,)
    position = models.CharField(_("Position"), max_length=100,)
    employee = models.ForeignKey(
        "employees.employee",
        verbose_name=_("Employee"),
        related_name="work_histories",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.position

    class Meta:
        verbose_name = _("Work History")
        verbose_name_plural = _("Work History")
