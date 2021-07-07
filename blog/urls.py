from django.urls import path
from .views import (
    article_list,
    ArticleDetailView,
    article_update_or_create_view,
    ArticleUpdateView,
    ArticleDeleteView,
)

app_name = 'blog'
urlpatterns = [
    path('', article_list, name='list-index'),
    path('p-<int:page>/', article_list, name='list'),
    path('create/', article_update_or_create_view, name='create'),
    path('<slug>/', ArticleDetailView.as_view(), name='detail'),
    path('<slug>/update/', article_update_or_create_view, name='update'),
    path('<slug>/delete/', ArticleDeleteView.as_view(), name='delete'),
]
