from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('maintenance-mode/', include('maintenance_mode.urls')),
    path('accounts/profile/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('tz_detect/', include('tz_detect.urls')),
    path('markdownx/', include('markdownx.urls')),
    path('', include('blog.urls')),
]  +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
