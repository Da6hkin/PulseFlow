from rest_framework import serializers

from pulse.models import ProjectManager
from pulse.serializers.employee_serializer import EmployeeDetailSerializer
from pulse.serializers.project_serializer import ProjectDetailSerializer


class ProjectManagerCreateSerializer(serializers.ModelSerializer):
    disabled = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = ProjectManager
        fields = ("employee", "project", "disabled",)


class ProjectManagerListSerializer(serializers.ModelSerializer):
    employee = EmployeeDetailSerializer(read_only=True)
    project = ProjectDetailSerializer(read_only=True)

    class Meta:
        model = ProjectManager
        fields = "__all__"


class ProjectManagerDetailSerializer(serializers.ModelSerializer):
    employee = EmployeeDetailSerializer(read_only=True)
    project = ProjectDetailSerializer(read_only=True)

    class Meta:
        model = ProjectManager
        fields = "__all__"
