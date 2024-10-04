from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('blog-detail/<int:pk>/', views.BlogDetail.as_view(), name='blog_detail'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('post/', views.CreateBlogPostView.as_view(), name='post'),
    path('post_done/', views.PostSuccessView.as_view(), name='post_done'),
]
