from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pulse.auth.authentication import JWTAuthentication
from pulse.filters.chat_message_filter import ChatMessageFilter
from pulse.models import ChatMessage
from pulse.serializers.chat_message_serializer import ChatMessageCreateSerializer, ChatMessageDetailSerializer, \
    ChatMessageUpdateSerializer, ChatMessageListSerializer
from pulse.serializers.error_serializer import DummyDetailSerializer, DummyDetailAndStatusSerializer


@extend_schema(tags=["Chat Message"])
@extend_schema_view(
    post=extend_schema(
        summary="Create chat message",
        request=ChatMessageCreateSerializer,
        responses={
            status.HTTP_200_OK: ChatMessageDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
)
class ChatMessageCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        chat_message = ChatMessageCreateSerializer(data=request.data)
        chat_message.is_valid(raise_exception=True)
        chat_message.save()
        return Response(chat_message.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Chat Message"])
@extend_schema_view(
    get=extend_schema(
        summary="Detailed info about chat message",
        responses={
            status.HTTP_200_OK: ChatMessageDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
    put=extend_schema(
        summary="Update chat message",
        request=ChatMessageUpdateSerializer,
        responses={
            status.HTTP_200_OK: ChatMessageDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
    delete=extend_schema(
        summary="Delete chat message",
        responses={
            status.HTTP_200_OK: DummyDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    )
)
class ChatMessageDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_chat_message(self, pk):
        try:
            return ChatMessage.objects.get(pk=pk)
        except ChatMessage.DoesNotExist:
            raise Http404("Chat message does not exist")

    def get(self, request, pk):
        chat_message = self.get_chat_message(pk)
        serializer = ChatMessageDetailSerializer(chat_message)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        chat_message = self.get_chat_message(pk)
        serializer = ChatMessageUpdateSerializer(chat_message, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        updated_chat_message = ChatMessageDetailSerializer(chat_message)
        return Response(updated_chat_message.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        chat_message = self.get_chat_message(pk)
        chat_message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Chat Message"])
@extend_schema_view(
    get=extend_schema(
        summary="Search chat messages",
        responses={
            status.HTTP_200_OK: ChatMessageListSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        }
    )
)
class ChatMessageListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ChatMessageFilter

    def get_queryset(self):
        chat_messages = ChatMessage.objects.all()
        return chat_messages
