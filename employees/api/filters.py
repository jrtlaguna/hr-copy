from django.db.models import Q

import django_filters as filters
from django_filters import FilterSet

from employees.models import Employee
from users.models import User


class EmployeeFilter(FilterSet):
    search = filters.CharFilter(method="_multi_search")

    def _multi_search(self, queryset, name, value):
        return queryset.filter(
            Q(user__email__icontains=value)
            | Q(user__first_name__icontains=value)
            | Q(user__middle_name__icontains=value)
            | Q(user__last_name__icontains=value)
            | Q(nickname__icontains=value)
        )

    class Meta:
        model = Employee
        fields = []
