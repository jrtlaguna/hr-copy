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
    EmployeeUpdateSerializer,
    EmergencyContactSerializer,
    WorkHistorySerializer,
)


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    filter_class = EmployeeFilter
    filter_backends = (filters.DjangoFilterBackend,)


    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == "PATCH" or self.request.method == "PUT":
            serializer_class = EmployeeUpdateSerializer
        
        return serializer_class

    def destroy(self, request, *args, **kwargs):
        
        instance = self.get_object()
        instance.user.is_active = False
        instance.user.save()

        return Response(status=status.HTTP_200_OK)