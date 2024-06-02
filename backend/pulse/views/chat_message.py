from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pulse.auth.authentication import JWTAuthentication
from pulse.filters.chat_message_filter import ChatMessageFilter
from pulse.models import ChatMessage, Employee, Project
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
        project = chat_message.validated_data["project"]
        user = chat_message.validated_data["user"]
        if user != request.user:
            raise Http404("You are not allowed to perform this request")
        try:
            employee = Employee.objects.get(user_id=user.id, company_id=project.company.id)
            if employee:
                chat_message.save()
                return Response(chat_message.data, status=status.HTTP_201_CREATED)
        except Project.DoesNotExist:
            raise Http404("Project does not exist")
        except Employee.DoesNotExist:
            raise Http404("You are not allowed to perform this request")


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
        user = self.request.user
        project_id = self.request.query_params.get('project', None)
        if project_id:
            try:
                project = Project.objects.get(id=project_id)
                Employee.objects.get(user_id=user.id, company=project.company)
                chat_messages = ChatMessage.objects.all()
                return chat_messages
            except Project.DoesNotExist:
                raise Http404("Project does not exist")
            except Employee.DoesNotExist:
                raise Http404("You do not have permission to perform this action.")
        else:
            raise Http404("You can't perform search without company parameter.")
