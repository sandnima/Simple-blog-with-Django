from django.views.generic import (
    TemplateView,
    ListView,
)
from django.db.models import Count
from blog.models import Article


class IndexView(ListView):
    template_name = 'index.html'
    queryset = Article.objects.all().annotate(likes_count=Count('liked')).order_by('-likes_count')
    
    
class AboutView(TemplateView):
    template_name = 'about.html'
