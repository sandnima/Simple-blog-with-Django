from django.urls import path
from .views import (
    dashboard,
    article_list,
    article_update_or_create,
    article_preview,
    ArticleDeleteView,
)

app_name = 'dashboard'
urlpatterns = [
    path('', dashboard, name='index'),
    path('blog/', article_list, name='article_list_index'),
    path('blog/p-<int:page>/', article_list, name='article_list'),
    path('blog/create/', article_update_or_create, name='create'),
    path('blog/<slug:slug>/update/', article_update_or_create, name='update'),
    path('blog/<slug:slug>/preview/', article_preview, name='preview'),
    path('blog/<slug:slug>/delete/', ArticleDeleteView.as_view(), name='delete'),
]
