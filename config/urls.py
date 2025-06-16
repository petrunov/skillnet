# config/urls.py

from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.shortcuts import redirect

schema_view = get_schema_view(
    openapi.Info(
        title="Skillnet API",
        default_version='v1',
        description="The skillned FE app depends on this API to enable user featuers.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def root_redirect(request):
    return redirect('schema-swagger-ui')

urlpatterns = [
    # Root → Swagger UI
    path('', root_redirect),

    # Swagger endpoints
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),

    # All account/auth endpoints live here
    path('api/accounts/', include('accounts.urls')),

    # Admin (if needed)
    path('admin/', admin.site.urls),
    
]
