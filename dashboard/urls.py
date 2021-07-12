from django.urls import path
from .views import (
    article_list,
    article_update_or_create_view,
    ArticleDeleteView,
)

app_name = 'dashboard'
urlpatterns = [
    # path('', dashboard, name='index'),
    path('blog/', article_list, name='article_list'),
    path('blog/create/', article_update_or_create_view, name='create'),
    path('blog/<slug>/update/', article_update_or_create_view, name='update'),
    path('blog/<slug>/delete/', ArticleDeleteView.as_view(), name='delete'),
]
