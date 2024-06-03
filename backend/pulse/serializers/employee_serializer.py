from rest_framework import serializers

from pulse.models import Employee, ProjectManager
from pulse.serializers.company_serializer import CompanyDetailSerializer
from pulse.serializers.user_serializer import UserDetailSerializer


class EmployeeCreateSerializer(serializers.ModelSerializer):
    disabled = serializers.BooleanField(required=False, default=False)
    is_admin = serializers.BooleanField(required=True)

    class Meta:
        model = Employee
        fields = ("user", "company", "is_admin", "disabled")


class EmployeeUpdateSerializer(serializers.ModelSerializer):
    disabled = serializers.BooleanField(required=False)

    class Meta:
        model = Employee
        fields = ("disabled",)


class EmployeeListSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    company = CompanyDetailSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeByCompanySerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    company = CompanyDetailSerializer(read_only=True)
    project_manager = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'user', 'company', 'is_admin', 'disabled', 'project_manager']

    def get_project_manager(self, obj):
        is_project_manager = ProjectManager.objects.filter(employee=obj).exists()
        return is_project_manager


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
