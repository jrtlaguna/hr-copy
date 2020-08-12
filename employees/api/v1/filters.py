from django_filters import FilterSet
from django_filters.filters import CharFilter

from django.db.models import Q

from employees.models import Employee
from users.models import User


class EmployeeFilter(FilterSet):
    search = CharFilter(method="_multi_search", label="name or email")

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
