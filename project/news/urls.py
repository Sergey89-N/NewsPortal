from django.urls import path, include
from .views import (NewsListView, NewsDetailView, NewsSearchView, NewsCreateView, NewsUpdateView, NewsDeleteView,
                    ArticleCreateView, ArticleUpdateView, ArticleDeleteView, ProfileUpdateView, become_author,
                    subscribe, unsubscribe)

urlpatterns = [
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('news/search/', NewsSearchView.as_view(), name='news_search'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('become-author/', become_author, name='become_author'),
    path('accounts/', include('allauth.urls')),
    path('category/<int:category_id>/subscribe/', subscribe, name='subscribe'),
    path('category/<int:category_id>/unsubscribe/', unsubscribe, name='unsubscribe'),
]
