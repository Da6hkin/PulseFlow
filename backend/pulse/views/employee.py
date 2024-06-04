from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pulse.auth.authentication import JWTAuthentication
from pulse.exceptions import SimplePermissionDenied
from pulse.filters.employee_filter import EmployeeFilter
from pulse.models import Employee, User, Company, Project, Task
from pulse.permissions import IsAssociatedWithEmployee, IsAssociatedWithCompany
from pulse.serializers.employee_serializer import EmployeeCreateSerializer, EmployeeDetailSerializer, \
    EmployeeUpdateSerializer, EmployeeListSerializer, AddEmployeeToCompanySerializer, EmployeeByCompanySerializer
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
        user = employee.validated_data.get('user')
        if request.user != user:
            raise SimplePermissionDenied()
        company = employee.validated_data.get("company")
        try:
            company = Company.objects.get(id=company.id)
            if request.user != company.creator:
                raise SimplePermissionDenied()
        except Company.DoesNotExist:
            raise Http404("Company does not exist")
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
    permission_classes = [IsAuthenticated, IsAssociatedWithEmployee]

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
    post=extend_schema(
        summary="Invite employee to company",
        request=AddEmployeeToCompanySerializer,
        responses={
            status.HTTP_200_OK: EmployeeDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
)
class EmployeeDetailViewAddToCompany(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddEmployeeToCompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        company_id = serializer.validated_data.get('company_id')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise Http404("User with given email does not exist")
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            raise Http404("Company with given id does not exist")
        try:
            existing_employee = Employee.objects.get(user_id=user.id, company_id=company.id)
            if existing_employee:
                raise Http404("Employee already exist in company")
        except Employee.DoesNotExist:
            try:
                Employee.objects.get(user_id=request.user.id, company_id=company.id)
            except Employee.DoesNotExist:
                raise Http404("You do not have permission to perform this action.")
            new_employee = Employee(user=user, company=company, is_admin=False, disabled=False)
            new_employee.save()
            saved_employee = EmployeeDetailSerializer(new_employee)
            return Response(saved_employee.data, status=status.HTTP_200_OK)


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
        user = self.request.user
        company = self.request.query_params.get('company', None)
        if company:
            try:
                Employee.objects.get(user_id=user.id, company_id=company)
                employees = Employee.objects.all()
                return employees
            except Employee.DoesNotExist:
                raise Http404("You do not have permission to perform this action.")
        else:
            raise Http404("You can't perform search without company parameter.")


@extend_schema(tags=["Employee"])
@extend_schema_view(
    get=extend_schema(
        summary="Get employees within company",
        responses={
            status.HTTP_200_OK: EmployeeByCompanySerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    )
)
class EmployeeListViewByCompany(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAssociatedWithCompany]

    def get_company(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404("Company does not exist")

    def get(self, request, pk):
        company = self.get_company(pk)
        employees = Employee.objects.filter(company=company)
        serializer = EmployeeByCompanySerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Employee"])
@extend_schema_view(
    get=extend_schema(
        summary="Detailed info about employee by task",
        responses={
            status.HTTP_200_OK: EmployeeDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
)
class EmployeeDetailViewByJWTTask(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_task(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404("Task does not exist")

    def get(self, request, task_id):
        task = self.get_task(task_id)
        try:
            employee = Employee.objects.get(user=request.user, company=task.project.company)
            serializer = EmployeeDetailSerializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            raise Http404("You are not part of company")
