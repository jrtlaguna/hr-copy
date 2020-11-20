import factory
from datetime import datetime, timedelta

from django.utils import timezone

from leaves.models import (
    Holiday,
    HolidayTemplate,
    HolidayType,
    LeaveAllocation,
    LeaveApplication,
    LeaveType,
)


class LeaveTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LeaveType

    name = "Unpaid"
    is_paid = False
    is_optional = False
    is_convertible_to_cash = False
    is_carry_forwarded = True


class LeaveAllocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LeaveAllocation

    from_date = datetime.strptime("2020-01-01", "%Y-%m-%d").date()
    to_date = datetime.strptime("2020-12-31", "%Y-%m-%d").date()
    count = 7
    notes = "Leave Allocation"


class LeaveApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LeaveApplication

    from_date = timezone.now().date()
    to_date = from_date + timedelta(2)


class HolidayFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Holiday

    name = "Fake Holiday"
    date = timezone.now().date()


class HolidayTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HolidayType

    name = "Special Non-working Holiday"
    is_no_work_no_pay = True
    pay_percentage = 0.3


class HolidayTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HolidayTemplate

    name = "Christmas"
    month = 12
    day = 25
