from calendar import monthrange

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel

from core.models import OPTIONAL
from employees.models import Employee


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
        return super().get_queryset().filter(is_active=True)


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


class HolidayType(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=100, unique=True)
    is_no_work_no_pay = models.BooleanField(_("Is No Work No Pay"), default=True)
    pay_percentage = models.FloatField(_("Pay Percentage"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Holiday Type")
        verbose_name_plural = _("Holiday Types")


class HolidayTemplate(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=150, unique=True)
    month = models.IntegerField(_("Month"),)
    day = models.IntegerField(_("Day"),)
    type = models.ForeignKey("leaves.HolidayType", verbose_name=_("Type"), related_name="holiday_templates", on_delete=models.CASCADE,)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = (_("Holiday Template"))
        verbose_name_plural = (_("Holiday Templates"))

    def clean(self):
        validations = {}

        day = self.day
        month = self.month
        if month not in range(1, 13):
            validations['month'] = ValidationError(
                _('Month field out of range.'),
                code='month-out-of-range',
            )

        # Need to raise validationerror here since monthrange will cause an error for wrong values
        if validations:
            raise ValidationError(validations)

        month_days = monthrange(2020, month)[1]
        if day not in range(1, month_days+1):
            validations['day'] = ValidationError(
                _('Day field out of range for month value.'),
                code='day-out-of-range',
            )

        if validations:
            raise ValidationError(validations)
