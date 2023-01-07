from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title='Services API',
        default_version='1.0.0',
        description='Services API documentation'
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include([
        path('', include('ClientManagement.urls')),
        path('', include('Mailing.urls')),
        path('docs', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema')
    ])),
]
