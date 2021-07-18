from django.urls import path
from .views import (
    article_list,
    ArticleDetailView,
)

app_name = 'blog'
urlpatterns = [
    path('', article_list, name='list-index'),
    path('p-<int:page>/', article_list, name='list'),
    path('<unicode_slug:slug>/', ArticleDetailView.as_view(), name='detail'),
]
