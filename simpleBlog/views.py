from django.views.generic import (
    TemplateView,
    ListView,
)
from django.db.models import Count
from blog.models import Article


class IndexView(ListView):
    template_name = 'index.html'
    # queryset = Article.objects.all().filter(status='PUB').annotate(likes_count=Count('liked')).order_by('-likes_count')
    queryset = Article.objects.all().filter(status='PUB').order_by('-updated_at')
    
    
class AboutView(TemplateView):
    template_name = 'about.html'
