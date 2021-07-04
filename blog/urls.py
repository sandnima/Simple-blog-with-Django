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
    path('<pk>/', ArticleDetailView.as_view(), name='detail'),
    path('<pk>/update/', ArticleUpdateView.as_view(), name='update'),
    path('<pk>/delete/', ArticleDeleteView.as_view(), name='delete'),
]
