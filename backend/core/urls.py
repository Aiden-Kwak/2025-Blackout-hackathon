from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path("api/accountapp/", include("myaccountapp.urls")),
    path("api/llmapp/", include("llmapp.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)