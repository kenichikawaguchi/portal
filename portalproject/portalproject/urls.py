from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from blog import views as blog_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('maintenance-mode/', include('maintenance_mode.urls')),
    path('accounts/profile/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('tz_detect/', include('tz_detect.urls')),
    path('markdownx/', include('markdownx.urls')),
    path('p5/', include('p5.urls')),
]  +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
## urlpatterns.append(re_path(r'^.*$', blog_views.MiscView.as_view(), name='misc'))
