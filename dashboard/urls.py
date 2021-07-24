from django.urls import path
from .views import (
    DashboardIndexView,
    DashboardArticleListView,
    DashboardArticleCreateView,
    DashboardArticleUpdateView,
    article_preview,
    ArticleDeleteView,
)

app_name = 'dashboard'
urlpatterns = [
    path('', DashboardIndexView.as_view(), name='index'),
    path('blog/', DashboardArticleListView.as_view(), name='article_list_index'),
    path('blog/p-<int:page>/', DashboardArticleListView.as_view(), name='article_list'),
    path('blog/create/', DashboardArticleCreateView.as_view(), name='article_create'),
    path('blog/<unicode_slug:slug>/update/', DashboardArticleUpdateView.as_view(), name='article_update'),
    path('blog/<unicode_slug:slug>/preview/', article_preview, name='article_preview'),
    path('blog/<unicode_slug:slug>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
]
