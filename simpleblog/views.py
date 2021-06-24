from django.views.generic import (
    TemplateView,
    ListView,
)
from blog.models import Article


class IndexView(ListView):
    template_name = 'index.html'
    queryset = Article.objects.all()
    

class AboutView(TemplateView):
    template_name = 'about.html'
