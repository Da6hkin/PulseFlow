from rest_framework import serializers

from pulse.models import ChatMessage
from pulse.serializers.project_serializer import ProjectDetailSerializer
from pulse.serializers.user_serializer import UserDetailSerializer


class ChatMessageCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(required=False)

    class Meta:
        model = ChatMessage
        fields = "__all__"


class ChatMessageUpdateSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=False, max_length=1000)

    class Meta:
        model = ChatMessage
        fields = ("text",)


class ChatMessageListSerializer(serializers.ModelSerializer):
    project = ProjectDetailSerializer(read_only=True)
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = "__all__"


class ChatMessageDetailSerializer(serializers.ModelSerializer):
    project = ProjectDetailSerializer(read_only=True)
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = "__all__"
