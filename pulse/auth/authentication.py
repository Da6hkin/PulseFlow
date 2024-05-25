from datetime import datetime, timedelta
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None

        jwt_token = JWTAuthentication.get_the_token_from_header(jwt_token)

        try:
            payload = jwt.decode(jwt_token, settings.JWT_CONF['SECRET_KEY'],
                                 algorithms=[settings.JWT_CONF['ALGORITHM']])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except:
            raise ParseError()

        user_email = payload.get('user_email')
        if user_email is None:
            raise AuthenticationFailed('User identifier not found in JWT')

        user = User.objects.filter(email=user_email).first()
        if user is None:
            raise AuthenticationFailed('User not found')

        return user, payload

    def authenticate_header(self, request):
        return 'Bearer'

    @classmethod
    def create_jwt(cls, user):

        payload = {
            'user_email': user.email,
            'exp': int((datetime.now() + timedelta(hours=settings.JWT_CONF['TOKEN_LIFETIME_HOURS'])).timestamp()),
            'iat': datetime.now().timestamp(),
            'name': user.name,
        }

        jwt_token = jwt.encode(payload, settings.JWT_CONF['SECRET_KEY'], algorithm=settings.JWT_CONF['ALGORITHM'])

        return jwt_token

    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '')
        return token


class TokenScheme(OpenApiAuthenticationExtension):
    target_class = 'pulse.auth.authentication.JWTAuthentication'
    name = 'jwtAuth'
    match_subclasses = True
    priority = -1

    def get_security_definition(self, auto_schema):
        return build_bearer_security_scheme_object(
            header_name='Authorization',
            token_prefix="Bearer",
        )
