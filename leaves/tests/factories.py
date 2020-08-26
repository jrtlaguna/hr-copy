import factory

from django.utils import timezone

from leaves.models import (
    LeaveAllocation,
    LeaveApplication,
    LeaveType,
    Holiday,
    HolidayType,
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

    from_date = "2020-01-01"
    to_date = "2020-12-12"
    count = 7
    notes = "Leave Allocation"


class LeaveApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LeaveApplication

    from_date = "2020-08-17"
    to_date = "2020-08-20"


class HolidayFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Holiday

    name = "Fake Holiday"
    date = timezone.now().date()


class HolidayTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HolidayType

    is_no_work_no_pay = True
    pay_percentage = 0.3
