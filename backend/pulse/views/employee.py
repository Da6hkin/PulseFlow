from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pulse.auth.authentication import JWTAuthentication
from pulse.filters.employee_filter import EmployeeFilter
from pulse.models import Employee
from pulse.serializers.employee_serializer import EmployeeCreateSerializer, EmployeeDetailSerializer, \
    EmployeeUpdateSerializer, EmployeeListSerializer
from pulse.serializers.error_serializer import DummyDetailSerializer, DummyDetailAndStatusSerializer


@extend_schema(tags=["Employee"])
@extend_schema_view(
    post=extend_schema(
        summary="Create employee",
        request=EmployeeCreateSerializer,
        responses={
            status.HTTP_200_OK: EmployeeDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
)
class EmployeeCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        employee = EmployeeCreateSerializer(data=request.data)
        employee.is_valid(raise_exception=True)
        employee.save()
        return Response(employee.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Employee"])
@extend_schema_view(
    get=extend_schema(
        summary="Detailed info about employee",
        responses={
            status.HTTP_200_OK: EmployeeDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
    put=extend_schema(
        summary="Update employee",
        request=EmployeeUpdateSerializer,
        responses={
            status.HTTP_200_OK: EmployeeDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
    delete=extend_schema(
        summary="Disable employee",
        responses={
            status.HTTP_200_OK: DummyDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    )
)
class EmployeeDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_employee(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404("Employee does not exist")

    def get(self, request, pk):
        employee = self.get_employee(pk)
        serializer = EmployeeDetailSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        employee = self.get_employee(pk)
        serializer = EmployeeUpdateSerializer(employee, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        updated_employee = EmployeeDetailSerializer(employee)
        return Response(updated_employee.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        employee = self.get_employee(pk)
        employee.disabled = True
        employee.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Employee"])
@extend_schema_view(
    get=extend_schema(
        summary="Search employees",
        responses={
            status.HTTP_200_OK: EmployeeListSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        }
    )
)
class EmployeeListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Employee.objects.all()
    serializer_class = EmployeeListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EmployeeFilter

    def get_queryset(self):
        employees = Employee.objects.all()
        return employees


