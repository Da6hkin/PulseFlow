from django.urls import path

from pulse.views.auth import CustomTokenObtainPairView
from pulse.views.user import *

urlpatterns = [
    path('/login', CustomTokenObtainPairView.as_view()),
]
