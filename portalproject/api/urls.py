from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, CategoryViewSet


router = DefaultRouter()
router.register(r'blogpost', BlogPostViewSet)
router.register(r'category', CategoryViewSet)

urlpatterns = router.urls

