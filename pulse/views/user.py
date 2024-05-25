from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password

from pulse.auth.authentication import JWTAuthentication
from pulse.filters.user_filter import UserFilter
from pulse.models import User
from pulse.serializers.error_serializer import DummyDetailSerializer, DummyDetailAndStatusSerializer
from pulse.serializers.user_serializer import UserListSerializer, UserDetailSerializer, UserCreateSerializer, \
    UserUpdateSerializer


@extend_schema(tags=["Users"])
@extend_schema_view(
    get=extend_schema(
        summary="Detailed info about user",
        responses={
            status.HTTP_200_OK: UserDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
    put=extend_schema(
        summary="Update user",
        request=UserUpdateSerializer,
        responses={
            status.HTTP_200_OK: UserDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
    delete=extend_schema(
        summary="Disable user",
        responses={
            status.HTTP_200_OK: DummyDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    )
)
class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404("User does not exist")

    def get(self, request, pk):
        user = self.get_user(pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = self.get_user(pk)
        serializer = UserUpdateSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.password = make_password(serializer.password)
        serializer.save()
        updated_user = UserDetailSerializer(user)
        return Response(updated_user.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        user = self.get_user(pk)
        user.disabled = True
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Users"])
@extend_schema_view(
    post=extend_schema(
        summary="Create user",
        request=UserCreateSerializer,
        responses={
            status.HTTP_200_OK: UserDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        }
    )
)
class UserCreateView(APIView):
    def post(self, request):
        user = UserCreateSerializer(data=request.data)
        user.is_valid(raise_exception=True)
        saved_user = user.save()
        return_data = {
            "name": saved_user.name,
            "surname": saved_user.surname,
            "email": saved_user.email,
            "disabled": saved_user.disabled
        }
        return Response(return_data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Users"])
@extend_schema_view(
    get=extend_schema(
        summary="Search users",
        responses={
            status.HTTP_200_OK: UserListSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        }
    )
)
class UserListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter

    def get_queryset(self):
        users = User.objects.all()
        return users
