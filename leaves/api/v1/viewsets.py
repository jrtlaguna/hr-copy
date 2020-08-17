from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from leaves.api.v1.filters import (
    LeaveAllocationFilter,
    LeaveApplicationFilter,
    LeaveTypeFilter,
)
from leaves.api.v1.serializers import (
    LeaveAllocationSerializer,
    LeaveApplicationSerializer,
    LeaveTypeSerializer,
)
from leaves.models import (
    LeaveAllocation,
    LeaveApplication,
    LeaveType,
)


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


class LeaveApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveApplicationSerializer
    queryset = LeaveApplication.objects.all()
    filter_class = LeaveApplicationFilter
    filter_backends = (filters.DjangoFilterBackend,)
    http_method_names = ["get", "post", "head", "put", "patch"]

    def perform_create(self, serializer):
        try:
            data = serializer.validated_data

            employee = data.get("employee")
            leave_type = data.get("leave_type")
            leave_allocations = employee.leave_allocations.filter(
                leave_type=leave_type, is_active=True, count__gt=0
            ).all()

            if not leave_allocations:
                raise ValidationError("Insufficient Leave Allocation")
            return super().perform_create(serializer)

        except Exception as e:
            raise ValidationError(e)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):

        application = self.get_object()
        application.status = "open"
        application.save()

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):

        application = self.get_object()
        application.status = "approved"
        application.save()

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def decline(self, request, pk=None):

        application = self.get_object()
        application.status = "declined"
        application.save()

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):

        application = self.get_object()
        application.status = "cancelled"
        application.save()

        return Response(status=status.HTTP_200_OK)
