from django.contrib.auth.backends import BaseBackend
from rest_framework import authentication
from rest_framework import exceptions

from django.contrib.auth.hashers import check_password

from pulse.models import User


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return None

        try:
            user = User.objects.get(email=email)
            if user.disabled:
                raise exceptions.AuthenticationFailed('This account has been disabled.')
            if not check_password(password, user.password):
                raise exceptions.AuthenticationFailed('Incorrect credentials.')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user.')

        return user, None
