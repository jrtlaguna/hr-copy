from django_extensions.db.models import TimeStampedModel

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import OPTIONAL
from employees.models import Employee


class LeaveApplication(TimeStampedModel):

    STATUS_DRAFT = "draft"
    STATUS_OPEN = "open"
    STATUS_APPROVED = "approved"
    STATUS_DECLINED = "declined"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = (
        (STATUS_DRAFT, "draft"),
        (STATUS_OPEN, "open"),
        (STATUS_APPROVED, "approved"),
        (STATUS_DECLINED, "declined"),
        (STATUS_CANCELLED, "cancelled"),
    )

    approver = models.ForeignKey(
        "employees.employee",
        verbose_name=_("Approver"),
        related_name="approver_leave_applications",
        on_delete=models.PROTECT,
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

    def __str__(self):
        return self.employee.user.get_full_name()

    class Meta:
        verbose_name = _("Leave Allocation")
        verbose_name_plural = _("Leave Allocations")
