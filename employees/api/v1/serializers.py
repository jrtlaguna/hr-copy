from django_restql.mixins import DynamicFieldsMixin
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from employees.models import (
    Employee,
    EmergencyContact,
    WorkHistory,
    Education,
)
from users.models import User
from users.api.v1.serializers import UserSerializer


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        exclude = ("employee",)


class WorkHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkHistory
        exclude = ("employee",)


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ("employee",)


class EmployeeSerializer(DynamicFieldsMixin, WritableNestedModelSerializer):
    user = UserSerializer(partial=True)
    work_histories = WorkHistorySerializer(many=True, required=False)
    emergency_contacts = EmergencyContactSerializer(many=True, required=False)
    educations = EducationSerializer(many=True, required=False)

    class Meta:
        model = Employee
        fields = "__all__"

    def update_or_create_direct_relations(self, attrs, relations):
        # Create or update direct relations (foreign key, one-to-one)
        request = self.context.get("request")

        if request.method in ("PATCH", "PUT"):
            for field_name, (field, field_source) in relations.items():
                obj = None
                data = self.get_initial()[field_name]
                model_class = field.Meta.model

                # Fix for WritableNestedModelSerializer NestedCreateMixin default behavior
                # Prevents creation of a new related instance if pk is not supplied
                # Set to always use the pk of the related instance for update
                pk = self._get_related_pk(
                    {
                        model_class._meta.pk.attname: getattr(
                            self.instance, field_name
                        ).pk
                    },
                    model_class,
                )

                if pk:
                    obj = model_class.objects.filter(pk=pk,).first()
                serializer = self._get_serializer_for_field(
                    field, instance=obj, data=data,
                )
                try:
                    serializer.is_valid(raise_exception=True)
                    attrs[field_source] = serializer.save(
                        **self._get_save_kwargs(field_name)
                    )
                except ValidationError as exc:
                    raise ValidationError({field_name: exc.detail})

        else:
            return super().update_or_create_direct_relations(attrs, relations)

