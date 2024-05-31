from rest_framework import serializers

from pulse.models import Assigned, RATE_TYPES
from pulse.serializers.employee_serializer import EmployeeDetailSerializer
from pulse.serializers.task_serializer import TaskDetailSerializer


class AssignedCreateSerializer(serializers.ModelSerializer):
    rate_type = serializers.ChoiceField(choices=RATE_TYPES)

    class Meta:
        model = Assigned
        fields = "__all__"


class AssignedUpdateSerializer(serializers.ModelSerializer):
    rate_type = serializers.ChoiceField(required=False, choices=RATE_TYPES)
    rate = serializers.FloatField(required=False)

    class Meta:
        model = Assigned
        fields = ("rate_type", "rate",)


class AssignedListSerializer(serializers.ModelSerializer):
    task = TaskDetailSerializer(read_only=True)
    employee = EmployeeDetailSerializer(read_only=True)

    class Meta:
        model = Assigned
        fields = "__all__"


class AssignedDetailSerializer(serializers.ModelSerializer):
    task = TaskDetailSerializer(read_only=True)
    employee = EmployeeDetailSerializer(read_only=True)

    class Meta:
        model = Assigned
        fields = "__all__"
