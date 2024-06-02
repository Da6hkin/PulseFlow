from pulse.views.company import CompanyCreateView, CompanyDetailView, CompanyDetailViewByJWT
from django.urls import path

urlpatterns = [
    path('/<int:pk>', CompanyDetailView.as_view(), name="company-actions-by-pk"),
    path('', CompanyCreateView.as_view()),
    path('/me', CompanyDetailViewByJWT.as_view())
]
