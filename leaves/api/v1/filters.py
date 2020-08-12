from django_filters import FilterSet
from django_filters.filters import CharFilter

from django.db.models import Q

from leaves.models import LeaveType


class LeaveTypeFilter(FilterSet):
    search = CharFilter(method="_multi_search", label="name")

    def _multi_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value))

    class Meta:
        model = LeaveType
        fields = []
