import numpy as np
from datetime import datetime, timedelta

from django_extensions.db.models import TimeStampedModel

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from core.models import OPTIONAL


class LeaveApplication(TimeStampedModel):

    STATUS_DRAFT = "draft"
    STATUS_SUBMITTED = "submitted"
    STATUS_APPROVED = "approved"
    STATUS_DECLINED = "declined"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = (
        (STATUS_DRAFT, "draft"),
        (STATUS_SUBMITTED, "submitted"),
        (STATUS_APPROVED, "approved"),
        (STATUS_DECLINED, "declined"),
        (STATUS_CANCELLED, "cancelled"),
    )

    approvers = models.ManyToManyField(
        "employees.employee",
        verbose_name=_("Approver"),
        related_name="approver_leave_applications",
    )
    employee = models.ForeignKey(
        "employees.employee",
        verbose_name=_("Employee"),
        related_name="employee_leave_applications",
        on_delete=models.PROTECT,
    )
    leave_type = models.ForeignKey(
        "leaves.LeaveType",
        verbose_name=_("Leave Type"),
        related_name="leave_applications",
        on_delete=models.PROTECT,
    )
    from_date = models.DateField(_("From Date"),)
    to_date = models.DateField(_("To Date"),)
    count = models.IntegerField(_("Count"), validators=[MinValueValidator(0),], default=0)
    reason = models.TextField(_("Reason"),)
    status = models.CharField(
        _("Status"), choices=STATUS_CHOICES, default=STATUS_DRAFT, max_length=50,
    )

    def __str__(self):
        return self.employee.user.get_full_name()

    class Meta:
        verbose_name = _("Leave Application")
        verbose_name_plural = _("Leave Applications")


    @property
    def for_submission_status(self):
        status = [self.STATUS_DRAFT]
        return status

    @property
    def for_approval_status(self):
        status = [self.STATUS_SUBMITTED]
        return status

    @property
    def for_decline_status(self):
        status = [self.STATUS_SUBMITTED]
        return status

    @property
    def for_cancellation_status(self):
        status = (
            LeaveApplication.STATUS_DRAFT,
            LeaveApplication.STATUS_SUBMITTED,
        )
        return status


class LeaveType(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=50,)
    is_active = models.BooleanField(_("Is Active"), default=True)
    is_paid = models.BooleanField(_("Is Paid"),)
    is_optional = models.BooleanField(_("Is Optional"),)
    is_convertible_to_cash = models.BooleanField(_("Is Convertible To Cash"),)
    is_carry_forwarded = models.BooleanField(_("Is Carry Forwarded"),)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Leave Type")
        verbose_name_plural = _("Leave Types")


class LeaveAllocationManager(models.Manager):
    def active(self):
        year = timezone.now().date().year
        return self.get_queryset().filter(
            is_active=True,
            from_date__year=year,
            to_date__year=year
            )


class LeaveAllocation(TimeStampedModel):
    employee = models.ForeignKey(
        "employees.employee",
        verbose_name=_("Employee"),
        related_name="leave_allocations",
        on_delete=models.PROTECT,
    )
    leave_type = models.ForeignKey(
        "leaves.LeaveType",
        verbose_name=_("Leave Type"),
        related_name="leave_allocations",
        on_delete=models.PROTECT,
    )
    is_active = models.BooleanField(_("Is Active"), default=True)
    from_date = models.DateField(_("From Date"),)
    to_date = models.DateField(_("To Date"),)
    count = models.IntegerField(_("Count"), validators=[MinValueValidator(0),],)
    notes = models.TextField(_("Notes"), **OPTIONAL)
    objects = LeaveAllocationManager()

    def __str__(self):
        return self.employee.user.get_full_name()

    class Meta:
        verbose_name = _("Leave Allocation")
        verbose_name_plural = _("Leave Allocations")


class Holiday(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=100)
    date = models.DateField(_("Date"),)
    type = models.ForeignKey(
        "leaves.HolidayType",
        verbose_name=_("Holiday Type"),
        related_name="holidays",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Holiday")
        verbose_name_plural = _("Holidays")

    @classmethod
    def business_days_count(cls, from_date: datetime, to_date: datetime) -> int:
        start_date = from_date 
        end_date = to_date + timedelta(1)
        holidays = cls.objects.values_list("date", flat=True)
        days = np.busday_count(start_date, end_date, holidays=holidays)
        return days.item()


class HolidayType(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=100, unique=True)
    is_no_work_no_pay = models.BooleanField(_("Is No Work No Pay"), default=True)
    pay_percentage = models.FloatField(_("Pay Percentage"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Holiday Type")
        verbose_name_plural = _("Holiday Types")
