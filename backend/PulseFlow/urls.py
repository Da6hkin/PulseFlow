from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from pulse.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user', include('pulse.urls.user_urls')),
    path('api/employee', include('pulse.urls.employee_urls')),
    path('api/project', include('pulse.urls.project_urls')),
    path('api/pm', include('pulse.urls.project_manager_urls')),
    path('api/auth', include('pulse.urls.auth_urls')),
    path('api/company', include('pulse.urls.company_urls')),
    path('api/task', include('pulse.urls.task_urls')),
    path('api/assigned', include('pulse.urls.assigned_urls')),
    path('api/chat', include('pulse.urls.chat_message_urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]
