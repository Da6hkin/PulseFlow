from rest_framework import serializers

from pulse.models import Task, STATE
from pulse.serializers.project_serializer import ProjectDetailSerializer


class TaskCreateSerializer(serializers.ModelSerializer):
    state = serializers.ChoiceField(choices=STATE)
    priority = serializers.IntegerField(required=False, min_value=1, max_value=5)
    actual_start_date = serializers.DateTimeField(required=False)
    actual_end_date = serializers.DateTimeField(required=False)

    class Meta:
        model = Task
        fields = "__all__"


class TaskUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    state = serializers.ChoiceField(required=False, choices=STATE)
    priority = serializers.IntegerField(required=False, min_value=1, max_value=5)
    description = serializers.CharField(required=False)
    planned_start_date = serializers.DateTimeField(required=False)
    planned_end_date = serializers.DateTimeField(required=False)
    actual_start_date = serializers.DateTimeField(required=False)
    actual_end_date = serializers.DateTimeField(required=False)

    class Meta:
        model = Task
        fields = (
            "name", "state", "priority", "description", "planned_start_date", "planned_end_date", "actual_start_date",
            "actual_end_date",)


class TaskListSerializer(serializers.ModelSerializer):
    project = ProjectDetailSerializer(read_only=True)

    class Meta:
        model = Task
        fields = "__all__"


class TaskDetailSerializer(serializers.ModelSerializer):
    project = ProjectDetailSerializer(read_only=True)

    class Meta:
        model = Task
        fields = "__all__"
