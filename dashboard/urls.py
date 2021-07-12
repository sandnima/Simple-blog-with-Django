from django.urls import path
from .views import (
    article_update_or_create_view,
    ArticleDeleteView,
)

app_name = 'dashboard'
urlpatterns = [
    # path('', article_list, name='list-index'),
    path('create/', article_update_or_create_view, name='create'),
    path('<slug>/update/', article_update_or_create_view, name='update'),
    path('<slug>/delete/', ArticleDeleteView.as_view(), name='delete'),
]
