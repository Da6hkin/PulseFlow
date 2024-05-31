from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pulse.auth.authentication import JWTAuthentication
from pulse.filters.company_filter import CompanyFilter
from pulse.models import Company, Employee
from pulse.serializers.company_serializer import CompanyDetailSerializer, CompanyListSerializer, CompanyUpdateSerializer
from pulse.serializers.error_serializer import DummyDetailSerializer, DummyDetailAndStatusSerializer


@extend_schema(tags=["Company"])
@extend_schema(
    summary="Create company",
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'name': {'type': 'string', 'example': 'Company Name'},
                'unique_identifier': {'type': 'string', 'example': 'unique-id-123'},
                'website': {'type': 'string', 'example': 'https://www.example.com'},
                'logo': {'type': 'string', 'format': 'binary'}
            },
            'required': ['name', 'unique_identifier']
        }
    },
    responses={
        status.HTTP_201_CREATED: CompanyDetailSerializer,
        status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
        status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
        status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
    },
)
class CompanyCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        company = CompanyDetailSerializer(data=request.data)
        company.is_valid(raise_exception=True)
        company.save()
        return Response(company.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Company"])
@extend_schema_view(
    get=extend_schema(
        summary="Detailed info about company",
        responses={
            status.HTTP_200_OK: CompanyDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
    put=extend_schema(
        summary="Update company",
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': 'New Company Name'},
                    'website': {'type': 'string', 'example': 'https://www.example_new.com'},
                    'logo': {'type': 'string', 'format': 'binary'}
                },
                'required': []
            }
        },
        responses={
            status.HTTP_200_OK: CompanyDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
)
class CompanyDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_company(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404("Company does not exist")

    def get(self, request, pk):
        user = self.get_company(pk)
        serializer = CompanyDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, pk):
        company = self.get_company(pk)
        serializer = CompanyUpdateSerializer(company, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        updated_company = CompanyDetailSerializer(company)
        return Response(updated_company.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Company"])
@extend_schema_view(
    get=extend_schema(
        summary="Search companies",
        responses={
            status.HTTP_200_OK: CompanyListSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        }
    )
)
class CompanyListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Company.objects.all()
    serializer_class = CompanyListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CompanyFilter

    def get_queryset(self):
        users = Company.objects.all()
        return users


@extend_schema(tags=["Company"])
@extend_schema_view(
    get=extend_schema(
        summary="Get companies by jwt",
        responses={
            status.HTTP_200_OK: CompanyListSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
)
class CompanyDetailViewByJWT(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        employees = Employee.objects.filter(user_id=user.id)
        companies = Company.objects.filter(id__in=employees.values('company_id'))
        serializer = CompanyListSerializer(companies,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
