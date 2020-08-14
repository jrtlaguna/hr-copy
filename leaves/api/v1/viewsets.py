from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.response import Response

from leaves.api.v1.filters import LeaveAllocationFilter, LeaveTypeFilter
from leaves.api.v1.serializers import LeaveAllocationSerializer, LeaveTypeSerializer
from leaves.models import LeaveAllocation, LeaveType


class LeaveTypeViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveTypeSerializer
    queryset = LeaveType.objects.all()
    filter_class = LeaveTypeFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        instance.is_active = False
        instance.save()

        return Response(status=status.HTTP_200_OK)


class LeaveAllocationViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveAllocationSerializer
    queryset = LeaveAllocation.objects.all()
    filter_class = LeaveAllocationFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        instance.is_active = False
        instance.save()

        return Response(status=status.HTTP_200_OK)
