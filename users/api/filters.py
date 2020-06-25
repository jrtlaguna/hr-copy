from django.db.models import Q

import django_filters as filters
from django_filters import FilterSet

from users.models import Employee, User

class EmployeeFilter(FilterSet):
    nickname = filters.CharFilter('nickname', lookup_expr='icontains')

    class Meta:
        fields = ['nickname']
        model = Employee


    