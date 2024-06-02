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
from pulse.permissions import IsAssociatedWithCompany
from pulse.serializers.company_serializer import CompanyDetailSerializer, CompanyListSerializer, CompanyUpdateSerializer
from pulse.serializers.error_serializer import DummyDetailSerializer, DummyDetailAndStatusSerializer


@extend_schema(tags=["Company"])
@extend_schema_view(
    post=extend_schema(
        summary="Create company",
        request=CompanyDetailSerializer,
        responses={
            status.HTTP_200_OK: CompanyDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
)
class CompanyCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
        request=CompanyUpdateSerializer,
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
    permission_classes = [IsAuthenticated, IsAssociatedWithCompany]

    def get_company(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404("Company does not exist")

    def get(self, request, pk):
        user = self.get_company(pk)
        serializer = CompanyDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        companies = Company.objects.filter(id__in=employees.values('company_id')) | Company.objects.filter(creator=user)
        serializer = CompanyListSerializer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
