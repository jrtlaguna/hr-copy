from datetime import datetime

from django.db import models
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from core.models import OPTIONAL
from leaves.models import LeaveApplication


class Employee(models.Model):

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
    )

    user = models.OneToOneField(
        "users.User",
        verbose_name=_("User"),
        related_name="employee",
        on_delete=models.CASCADE,
    )

    gender = models.CharField(_("Gender"), choices=GENDER_CHOICES, max_length=50,)
    date_of_birth = models.DateField(_("Date of Birth"), **OPTIONAL,)
    contact_number = models.CharField(_("Contact No."), max_length=100,)
    address = models.TextField(_("Adress"),)
    date_started = models.DateField(_("Date Started"), **OPTIONAL,)
    nickname = models.CharField(_("Nickname"), max_length=100, **OPTIONAL,)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    @property
    def remaining_leave_allocations(self):
        year = timezone.now().date().year
        approved_leaves = self.employee_leave_applications.filter(
                status=LeaveApplication.STATUS_APPROVED,
                from_date__year=year,
                to_date__year=year
            ).values("leave_type").annotate(
                total_approved=models.Sum("count")
            )
        approved_subquery = approved_leaves.filter(leave_type=models.OuterRef("leave_type"))
        allocations = self.leave_allocations.active().values("leave_type").annotate(
                total_allocation=models.Sum("count")
            ).annotate(
                total_approved=models.Subquery(approved_subquery.values("total_approved"), 
                output_field=models.IntegerField())
            ).annotate(
                remaining=models.F("total_allocation") - Coalesce(models.F("total_approved"), 0)
            )
        return allocations


class EmergencyContact(models.Model):

    name = models.CharField(_("Name"), max_length=100,)
    contact_number = models.CharField(_("Contact No."), max_length=100,)
    relation = models.CharField(_("Relation"), max_length=50, **OPTIONAL,)
    employee = models.ForeignKey(
        "employees.employee",
        verbose_name=_("Employee"),
        related_name="emergency_contacts",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Emergency Contact")
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
        verbose_name_plural = _("Educations")


class WorkHistory(models.Model):
    company = models.CharField(_("Company"), max_length=100,)
    position = models.CharField(_("Position"), max_length=100,)
    date_started = models.DateField(_("Date Started"), **OPTIONAL,)
    date_ended = models.DateField(_("Date Ended"), **OPTIONAL,)
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
        verbose_name_plural = _("Work Histories")
