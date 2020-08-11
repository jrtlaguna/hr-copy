from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.serializers import CustomWritableNestedModelSerializer
from leaves.models import LeaveType


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = "__all__"
