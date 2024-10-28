from django.urls import path

from . import views

app_name='accounts'

urlpatterns = [
    path('', views.UsernameChangeView.as_view(), name="update_username"),
]
