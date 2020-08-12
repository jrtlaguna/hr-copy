from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from leaves.models import LeaveType


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = "__all__"
