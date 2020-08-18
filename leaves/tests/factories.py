import factory

from leaves.models import (
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

    from_date = "2020-01-01"
    to_date = "2020-12-12"
    count = 7
    notes = "Leave Allocation"


class LeaveApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LeaveApplication

    from_date = "2020-08-17"
    to_date = "2020-08-20"
