from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from rest_framework import status, authentication
from rest_framework.response import Response

from pulse.auth.authentication import CustomAuthentication
from pulse.models import User
from pulse.serializers.auth_serializer import CustomTokenObtainPairSerializer, CustomTokenDetailSerializer
from pulse.serializers.error_serializer import DummyDetailSerializer, DummyDetailAndStatusSerializer


@extend_schema(tags=["Login"])
@extend_schema_view(
    post=extend_schema(
        summary="Issue Jwt",
        request=CustomTokenObtainPairSerializer,
        responses={
            status.HTTP_200_OK: CustomTokenDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        }
    )
)
class CustomTokenObtainPairView(TokenObtainPairView):
    authentication_classes = [CustomAuthentication]

    def post(self, request, *args, **kwargs):
        user = request.user
        if user is None:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

# class CustomJWTAuthentication(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         jwt_token = request.headers.get('Authorization', None)
#         if jwt_token is None:
#             raise exceptions.AuthenticationFailed('No token provided')
#         try:
#             untyped_token = UntypedToken(jwt_token.split(' ')[1])
#         except (InvalidToken, Exception) as e:
#             raise exceptions.AuthenticationFailed('Invalid token')
#
#         try:
#             email = untyped_token['email']  # Adjust the key according to your payload
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             raise exceptions.AuthenticationFailed('No such user')
#
#         # Assuming you have stored the user's email in the token, and you want to check it each time
#         if not user.password == untyped_token['email']:  # Adjust 'email' claim as per your token structure
#             raise exceptions.AuthenticationFailed('Email not matched')
#
#         # Return the user and token
#         return (user, untyped_token)
