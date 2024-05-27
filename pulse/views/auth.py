from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample
from rest_framework.response import Response
from rest_framework import views, permissions, status

from pulse.auth.authentication import JWTAuthentication
from pulse.serializers.auth_serializer import ObtainTokenSerializer, CustomTokenDetailSerializer
from pulse.serializers.error_serializer import DummyDetailSerializer, DummyDetailAndStatusSerializer

User = get_user_model()


@extend_schema(tags=["Login"])
@extend_schema_view(
    post=extend_schema(
        summary="Issue Jwt",
        request=ObtainTokenSerializer,
        responses={
            status.HTTP_200_OK: CustomTokenDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
        examples=[
            OpenApiExample(
                'Example',
                description="Example with default values",
                value={
                    'email': 'user@example.com',
                    'password': 'string',
                }
            )
        ],
        auth=[]
    )
)
class ObtainTokenView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ObtainTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        user = User.objects.filter(email=email).first()
        if user is None or not check_password(password, user.password):
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        jwt_token = JWTAuthentication.create_jwt(user)

        return Response({'token': jwt_token})
