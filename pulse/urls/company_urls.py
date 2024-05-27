from pulse.views.company import CompanyCreateView, CompanyDetailView, CompanyListView
from django.urls import path

urlpatterns = [
    path('/search', CompanyListView.as_view()),
    path('/<int:pk>', CompanyDetailView.as_view()),
    path('', CompanyCreateView.as_view()),
]
