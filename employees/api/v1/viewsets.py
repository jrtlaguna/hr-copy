from django_filters import rest_framework as filters
from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import EmployeeFilter
from employees.models import (
    Education,
    Employee,
    EmergencyContact,
    WorkHistory,
)
from employees.api.v1.serializers import (
    EducationSerializer,
    EmployeeSerializer,
    EmergencyContactSerializer,
    WorkHistorySerializer,
)


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    filter_class = EmployeeFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_active = False
            instance.user.is_active = False
            instance.save()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)
