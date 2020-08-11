from django.db.models import Q

import django_filters as filters
from django_filters import FilterSet

from leaves.models import LeaveType


class LeaveTypeFilter(FilterSet):
    search = filters.CharFilter(method="_multi_search", label="name")

    def _multi_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value))

    class Meta:
        model = LeaveType
        fields = []
