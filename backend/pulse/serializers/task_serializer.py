from rest_framework import serializers

from pulse.models import Task, STATE, Assigned
from pulse.serializers.project_serializer import ProjectDetailSerializer


class TaskCreateSerializer(serializers.ModelSerializer):
    state = serializers.ChoiceField(choices=STATE)
    priority = serializers.IntegerField(required=False, min_value=1, max_value=5)

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
    hours_spent = serializers.IntegerField(required=False)

    class Meta:
        model = Task
        fields = (
            "name", "state", "priority", "description", "planned_start_date", "planned_end_date", "hours_spent",)


class AssignedForTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assigned
        fields = "__all__"


class TaskListSerializer(serializers.ModelSerializer):
    project = ProjectDetailSerializer(read_only=True)
    assigned = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
        "id", "name", "project", "priority", "description", "planned_start_date", "planned_end_date", "assigned")

    def get_assigned(self, obj):
        assigned = Assigned.objects.filter(task=obj)
        return AssignedForTaskSerializer(assigned, many=True).data


class TaskDetailSerializer(serializers.ModelSerializer):
    project = ProjectDetailSerializer(read_only=True)

    class Meta:
        model = Task
        fields = "__all__"
