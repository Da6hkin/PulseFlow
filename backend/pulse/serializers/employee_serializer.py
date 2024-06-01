from rest_framework import serializers

from pulse.models import Employee
from pulse.serializers.company_serializer import CompanyDetailSerializer
from pulse.serializers.user_serializer import UserDetailSerializer


class EmployeeCreateSerializer(serializers.ModelSerializer):
    disabled = serializers.BooleanField(required=False, default=False)
    is_project_manager = serializers.BooleanField(required=True)

    class Meta:
        model = Employee
        fields = ("user", "company", "is_project_manager", "disabled")


class EmployeeUpdateSerializer(serializers.ModelSerializer):
    is_project_manager = serializers.BooleanField(required=False)

    class Meta:
        model = Employee
        fields = ("is_project_manager",)


class EmployeeListSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    company = CompanyDetailSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    company = CompanyDetailSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = "__all__"


class AddEmployeeToCompanySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    company_id = serializers.IntegerField(required=True)

    class Meta:
        model = Employee
        fields = ("email", "company_id",)
