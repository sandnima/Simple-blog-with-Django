from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    article_create_view,
    ArticleUpdateView,
    ArticleDeleteView,
)

app_name = 'blog'
urlpatterns = [
    path('', ArticleListView.as_view(), name='list'),
    path('create/', article_create_view, name='create'),
    path('<slug>/', ArticleDetailView.as_view(), name='detail'),
    path('<slug>/update/', ArticleUpdateView.as_view(), name='update'),
    path('<slug>/delete/', ArticleDeleteView.as_view(), name='delete'),
]
