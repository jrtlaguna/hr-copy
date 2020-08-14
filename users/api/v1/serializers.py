from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django_restql.mixins import DynamicFieldsMixin
from drf_writable_nested.mixins import UniqueFieldsMixin
from rest_framework import serializers

from users.models import User


class UserSerializer(
    UniqueFieldsMixin, DynamicFieldsMixin, serializers.ModelSerializer
):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "is_active",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.validated_data
        self._validate_unique_fields(validated_data)
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        return user

    def update(self, instance, validated_data):
        """
        Quick fix for UniqueFieldsMixin partial update if unique fields
        are not supplied in the payload.
        """
        for field_name in self._unique_fields:
            if not validated_data.get(field_name):
                validated_data[field_name] = getattr(instance, field_name)
        return super().update(instance, validated_data)
