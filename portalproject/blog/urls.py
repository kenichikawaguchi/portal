from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.CustomView.as_view(), name='index'),
    path('search/', views.CustomView.as_view(), name='search'),
    path('blog-detail/<int:pk>/', views.BlogDetail.as_view(), name='blog_detail'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact-sent/', views.ContactSentView.as_view(), name='contact_sent'),
    path('post/', views.CreateBlogPostView.as_view(), name='post'),
    path('post_done/', views.PostSuccessView.as_view(), name='post_done'),
    path('delete/<int:pk>/', views.BlogDeleteView.as_view(), name='delete'),
    path('update/<int:pk>/', views.UpdateBlogPostView.as_view(), name='update'),
    path('comment/create/<int:pk>/', views.CommentCreate.as_view(), name='comment_create'),
    path('comment/create2/<int:pk>/', views.CommentCreate2.as_view(), name='comment_create2'),
    path('comment-detail/<int:pk>/', views.CommentDetail.as_view(), name='comment_detail'),
    path('likes/<int:pk>/', views.LikesView.as_view(), name='likes'),
    path('likes/popup/<int:pk>/', views.LikesPopupView.as_view(), name='likes_popup'),
    path('likes/create/<int:blogpost_id>/<int:user_id>/', views.CreateLikeView.as_view(), name='likes_create'),
    path('likes/delete/<int:blogpost_id>/<int:user_id>/', views.DeleteLikeView.as_view(), name='likes_delete'),
]
