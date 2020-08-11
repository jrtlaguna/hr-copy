from datetime import datetime

import factory
from django.contrib.auth import get_user_model

from leaves.models import LeaveType


class LeaveTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LeaveType

    name = "Unpaid"
    is_paid = False
    is_optional = False
    is_convertible_to_cash = False
    is_carry_forwarded = True
