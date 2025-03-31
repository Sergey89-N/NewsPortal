from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post
from .serializers import PostSerializer

class NewsViewSet(viewsets.ModelViewSet):

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Выбираем новости с типом 'NW'
        return Post.objects.filter(post_type=Post.NEWS)

class ArticlesViewSet(viewsets.ModelViewSet):

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Выбираем статьи с типом 'AR'
        return Post.objects.filter(post_type=Post.ARTICLE)
