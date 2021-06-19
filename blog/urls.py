from django.urls import path
# from .views import list_view, detail_view
from .views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView

app_name = 'blog'
urlpatterns = [
    path('', ArticleListView.as_view(), name='list'),
    path('<int:id>/', ArticleDetailView.as_view(), name='detail'),
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('<int:id>/update/', ArticleUpdateView.as_view(), name='update'),
    path('<int:id>/delete/', ArticleDeleteView.as_view(), name='delete'),
]


'''
urlpatterns = [
    path('', list_view, name='list'),
    path('<int:id>', detail_view, name='detail'),
]
'''
