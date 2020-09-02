from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from django.db.models import F, Sum
from django.utils import timezone

from leaves.api.v1.filters import (
    HolidayFilter,
    LeaveAllocationFilter,
    LeaveApplicationFilter,
    LeaveTypeFilter,
)
from leaves.api.v1.serializers import (
    HolidaySerializer,
    HolidayTypeSerializer,
    LeaveAllocationSerializer,
    LeaveApplicationSerializer,
    LeaveTypeSerializer,
)
from leaves.models import (
    Holiday,
    HolidayType,
    LeaveAllocation,
    LeaveApplication,
    LeaveType,
)
from .permissions import LeaveApplicationApproverPermission


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

    @action(detail=True, url_path="submit", methods=["post"])
    def submit(self, request, pk=None):
        # for_submission_status = (LeaveApplication.STATUS_DRAFT,)
        application = self.get_object()
        if application.status in application.for_submission_status:
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
        detail=True,
        url_path="approve",
        methods=["post"],
        permission_classes=[IsAuthenticated, LeaveApplicationApproverPermission],
    )
    def approve(self, request, pk=None):
        application = self.get_object()
        leave_number_of_days = application.business_days_count
        if application.status in application.for_approval_status:

            employee = application.employee
            allocations = employee.leave_allocations_count
            
            for allocation in allocations:
                if allocation.get("leave_type") == application.leave_type.id:
                    if allocation.get("remaining") > leave_number_of_days:
                        application.status = LeaveApplication.STATUS_APPROVED
                        application.save()
                        serializer = self.get_serializer(application)
                        return Response(serializer.data)
                    else:
                        return Response(
                            {
                                "detail": f"Could not approve leave application, not enough leaves."
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
        return Response(
            {
                "detail": f"Could not approve leave application with status {application.status}"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=True,
        url_path="decline",
        methods=["post"],
        permission_classes=[IsAuthenticated, LeaveApplicationApproverPermission],
    )
    def decline(self, request, pk=None):
        application = self.get_object()
        if application.status in application.for_decline_status:
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
        application = self.get_object()
        if application.status in application.for_cancellation_status:
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


class HolidayViewSet(viewsets.ModelViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    filter_class = HolidayFilter
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAdminUser,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.date < timezone.now().date():
            return Response(
                {"message": "Can not delete holidays that have already passed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance.delete()
        return Response(status=status.HTTP_200_OK)


class HolidayTypeViewSet(viewsets.ModelViewSet):
    queryset = HolidayType.objects.all()
    serializer_class = HolidayTypeSerializer
    permission_classes = (IsAdminUser,)
