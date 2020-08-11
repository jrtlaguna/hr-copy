from django.http import Http404
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from leaves.api.v1.filters import LeaveTypeFilter
from leaves.api.v1.serializers import LeaveTypeSerializer
from leaves.models import LeaveType


class LeaveTypeViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveTypeSerializer
    queryset = LeaveType.objects.all()
    filter_class = LeaveTypeFilter
    filter_backends = (filters.DjangoFilterBackend,)
