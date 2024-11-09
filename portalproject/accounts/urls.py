from django.urls import path

from . import views

app_name='accounts'

urlpatterns = [
    path('', views.CustomUserView.as_view(), name="profile"),
    path('update_username/', views.UsernameChangeView.as_view(), name="update_username"),
    path('update_icon/', views.IconChangeView.as_view(), name="update_icon"),
    path('update_introduction/', views.IntroductionChangeView.as_view(), name="update_introduction"),
    path('target_user/', views.TargetUserView.as_view(), name="target_user"),
]
