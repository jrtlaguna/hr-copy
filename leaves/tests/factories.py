import factory

from employees.tests.factories import EmployeeFactory
from leaves.models import LeaveAllocation, LeaveType


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

    employee = factory.SubFactory(EmployeeFactory)
    leave_type = factory.SubFactory(LeaveTypeFactory)
    from_date = "2020-01-01"
    to_date = "2020-12-12"
    count = 7
    notes = "Leave Allocation"
