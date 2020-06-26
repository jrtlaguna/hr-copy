from django.db.models import Q

import django_filters as filters
from django_filters import FilterSet

from users.models import User


class UserFilter(FilterSet):
    class Meta:
        model = User
        exclude = ["password"]
