from django.urls import path

from pulse.views.auth import ObtainTokenView

urlpatterns = [
    path('/login', ObtainTokenView.as_view()),
]
