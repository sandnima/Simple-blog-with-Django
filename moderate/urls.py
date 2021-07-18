from django.urls import path
from .views import (
    moderate,
    article_list
)

app_name = 'moderate'
urlpatterns = [
    path('', moderate, name='index'),
    path('blog/', article_list, name='article_list_index'),
    path('blog/p-<int:page>/', article_list, name='article_list'),
]
