from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from django.db.models import F

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
from .permissions import LeaveApplicationPermission


class LeaveTypeViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveTypeSerializer
    queryset = LeaveType.objects.all()
    filter_class = LeaveTypeFilter
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAdminUser,)

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
    permission_classes = (IsAdminUser,)

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
    permission_classes = (LeaveApplicationPermission,)

    @action(detail=True, url_path="submit", methods=["post"])
    def submit(self, request, pk=None):
        for_submission_status = (LeaveApplication.STATUS_DRAFT,)
        application = self.get_object()
        if application.status in for_submission_status:
            application.status = LeaveApplication.STATUS_SUBMITTED
            application.save()
            serializer = self.get_serializer(application)
            return Response(serializer.data)
        return Response(
            {
                "detail": f"Could not submit leave application with status {application.status}"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=True, url_path="approve", methods=["post"],
    )
    def approve(self, request, pk=None):
        for_approval_status = (LeaveApplication.STATUS_SUBMITTED,)
        application = self.get_object()
        if application.status in for_approval_status:
            allocation = application.employee.leave_allocations.active().get(
                leave_type=application.leave_type
            )
            allocation.count = F("count") - 1
            application.status = LeaveApplication.STATUS_APPROVED
            application.save()
            serializer = self.get_serializer(application)
            return Response(serializer.data)
        return Response(
            {
                "detail": f"Could not approve leave application with status {application.status}"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=True, url_path="decline", methods=["post"],
    )
    def decline(self, request, pk=None):
        for_decline_status = (LeaveApplication.STATUS_SUBMITTED,)
        application = self.get_object()
        if application.status in for_decline_status:
            application.status = LeaveApplication.STATUS_DECLINED
            application.save()
            serializer = self.get_serializer(application)
            return Response(serializer.data)
        return Response(
            {
                "detail": f"Could not decline leave application with status {application.status}"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=True, url_path="cancel", methods=["post"])
    def cancel(self, request, pk=None):
        for_cancel_status = (
            LeaveApplication.STATUS_DRAFT,
            LeaveApplication.STATUS_SUBMITTED,
        )
        application = self.get_object()
        if application.status in for_cancel_status:
            application.status = LeaveApplication.STATUS_CANCELLED
            application.save()
            serializer = self.get_serializer(application)
            return Response(serializer.data)
        return Response(
            {
                "detail": f"Could not cancel leave application with status {application.status}"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
