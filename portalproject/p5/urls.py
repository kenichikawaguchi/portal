from django.urls import path

from . import views


app_name = 'p5'

urlpatterns = [
    path('', views.P5View.as_view(), name='p5'),
    path('tmp/<int:id>/', views.TmpView.as_view(), name='tmp'),
    path('<slug:appname>/', views.AppView.as_view(), name='app'),
]
