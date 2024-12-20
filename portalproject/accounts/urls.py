from django.urls import path

from . import views

app_name='accounts'

urlpatterns = [
    path('', views.CustomUserView.as_view(), name="profile"),
    path('update_username/', views.UsernameChangeView.as_view(), name="update_username"),
    path('update_icon/', views.IconChangeView.as_view(), name="update_icon"),
    path('update_introduction/', views.IntroductionChangeView.as_view(), name="update_introduction"),
    path('target_user/', views.TargetUserView.as_view(), name="target_user"),
    path('target_user/<slug:username>/', views.TargetUserView.as_view(), name="target_user_w_username"),
    path('<slug:username>', views.ProfileDetail.as_view(), name='profile_detail'),
    path('follow/<slug:username>/', views.follow_view, name='follow'),
    path('unfollow/<slug:username>/', views.unfollow_view, name='unfollow'),
    path('follow/popup/<slug:follow>/<slug:username>/', views.FollowPopupView.as_view(), name='follow_popup'),
    path('categories/', views.CategoriesView.as_view(), name="categories"),
    path('create_category/', views.CategoryCreateView.as_view(), name="create_category"),
    path('update_category/<int:pk>/', views.CategoryUpdateView.as_view(), name="update_category"),
    path('delete_category/<int:pk>/', views.CategoryDeleteView.as_view(), name="delete_category"),
]
