from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pulse.auth.authentication import JWTAuthentication
from pulse.filters.task_filter import TaskFilter
from pulse.models import Task
from pulse.serializers.error_serializer import DummyDetailSerializer, DummyDetailAndStatusSerializer
from pulse.serializers.task_serializer import TaskCreateSerializer, TaskDetailSerializer, TaskUpdateSerializer, \
    TaskListSerializer


@extend_schema(tags=["Task"])
@extend_schema_view(
    post=extend_schema(
        summary="Create task",
        request=TaskCreateSerializer,
        responses={
            status.HTTP_200_OK: TaskDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
)
class TaskCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        task = TaskCreateSerializer(data=request.data)
        task.is_valid(raise_exception=True)
        task.save()
        return Response(task.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Task"])
@extend_schema_view(
    get=extend_schema(
        summary="Detailed info about task",
        responses={
            status.HTTP_200_OK: TaskDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
    put=extend_schema(
        summary="Update task",
        request=TaskUpdateSerializer,
        responses={
            status.HTTP_200_OK: TaskDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
    delete=extend_schema(
        summary="Delete task",
        responses={
            status.HTTP_200_OK: DummyDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    )
)
class TaskDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_task(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404("Project does not exist")

    def get(self, request, pk):
        task = self.get_task(pk)
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        task = self.get_task(pk)
        serializer = TaskUpdateSerializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        updated_task = TaskDetailSerializer(task)
        return Response(updated_task.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        task = self.get_task(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Task"])
@extend_schema_view(
    get=extend_schema(
        summary="Search tasks",
        responses={
            status.HTTP_200_OK: TaskListSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        }
    )
)
class TaskListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_queryset(self):
        tasks = Task.objects.all()
        return tasks
