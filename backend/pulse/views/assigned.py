from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pulse.auth.authentication import JWTAuthentication
from pulse.filters.assigned_filter import AssignedFilter
from pulse.models import Assigned, Employee
from pulse.serializers.assigned_serializer import AssignedCreateSerializer, AssignedDetailSerializer, \
    AssignedUpdateSerializer, AssignedListSerializer
from pulse.serializers.error_serializer import DummyDetailSerializer, DummyDetailAndStatusSerializer


@extend_schema(tags=["Assigned"])
@extend_schema_view(
    post=extend_schema(
        summary="Create assigned",
        request=AssignedCreateSerializer,
        responses={
            status.HTTP_200_OK: AssignedDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
)
class AssignedCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        assigned = AssignedCreateSerializer(data=request.data)
        assigned.is_valid(raise_exception=True)
        assigned.save()
        return Response(assigned.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Assigned"])
@extend_schema_view(
    get=extend_schema(
        summary="Detailed info about assigned",
        responses={
            status.HTTP_200_OK: AssignedDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
    put=extend_schema(
        summary="Update assigned",
        request=AssignedUpdateSerializer,
        responses={
            status.HTTP_200_OK: AssignedDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
    delete=extend_schema(
        summary="Delete assigned",
        responses={
            status.HTTP_200_OK: DummyDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    )
)
class AssignedDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_assigned(self, pk):
        try:
            return Assigned.objects.get(pk=pk)
        except Assigned.DoesNotExist:
            raise Http404("Assigned does not exist")

    def get(self, request, pk):
        assigned = self.get_assigned(pk)
        serializer = AssignedDetailSerializer(assigned)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        assigned = self.get_assigned(pk)
        serializer = AssignedUpdateSerializer(assigned, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        updated_assigned = AssignedDetailSerializer(assigned)
        return Response(updated_assigned.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        assigned = self.get_assigned(pk)
        assigned.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Assigned"])
@extend_schema_view(
    get=extend_schema(
        summary="Search assigned",
        responses={
            status.HTTP_200_OK: AssignedListSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        }
    )
)
class AssignedListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Assigned.objects.all()
    serializer_class = AssignedListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AssignedFilter

    def get_queryset(self):
        assigned = Assigned.objects.all()
        return assigned


@extend_schema(tags=["Assigned"])
@extend_schema_view(
    get=extend_schema(
        summary="Check if user can change assigned",
        responses={
            status.HTTP_200_OK: AssignedDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    )
)
class AssignedDetailViewByJWT(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_assigned(self, pk):
        try:
            return Assigned.objects.get(pk=pk)
        except Assigned.DoesNotExist:
            raise Http404("Assigned does not exist")

    def get(self, request, pk):
        assigned = self.get_assigned(pk)
        user_id = request.user.id
        try:
            employee = Employee.objects.get(user_id=user_id, company_id=assigned.task.project.company.id)
        except Employee.DoesNotExist:
            raise Http404("User is not employee in this company")
        if assigned.employee == employee:
            return Response(True, status=status.HTTP_200_OK)
        else:
            return Response(False, status=status.HTTP_200_OK)
