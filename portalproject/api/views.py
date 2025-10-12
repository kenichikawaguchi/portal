from rest_framework import viewsets
from blog.models import BlogPost
from .serializers import BlogPostSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # ログインユーザーを自動設定

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)  # 更新時も必要なら

