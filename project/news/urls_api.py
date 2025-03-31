from rest_framework.routers import DefaultRouter
from .api_views import NewsViewSet, ArticlesViewSet

router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')
router.register(r'articles', ArticlesViewSet, basename='articles')

urlpatterns = router.urls
