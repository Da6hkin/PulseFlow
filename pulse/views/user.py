from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pulse.models import User
from pulse.serializers.error_serializer import DummyDetailSerializer, DummyDetailAndStatusSerializer
from pulse.serializers.user_serializer import UserListSerializer, UserDetailSerializer, UserCreateSerializer, \
    UserUpdateSerializer


@extend_schema(tags=["Users"])
@extend_schema_view(
    get=extend_schema(
        summary="Detailed info about All users",
        responses={
            status.HTTP_200_OK: UserDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        }
    )
)
class UserListView(APIView):
    def get(self, request):
        users = User.objects.filter()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        request=UserDetailSerializer,
        responses={
            status.HTTP_200_OK: DummyDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
    delete=extend_schema(
        summary="Delete user",
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
        serializer.save()
        updated_user = UserDetailSerializer(user)
        return Response(updated_user.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        user = self.get_user(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Users"])
@extend_schema_view(
    post=extend_schema(
        summary="Create user",
        request=UserCreateSerializer,
        responses={
            status.HTTP_200_OK: UserCreateSerializer,
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
        user.save()
        return Response(user.data, status=status.HTTP_201_CREATED)
