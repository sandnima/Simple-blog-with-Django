from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from django.views.generic import (
    DetailView,
)
from .models import (
    ApprovedArticle,
)


def article_list(request, page=1):
    template_name = 'blog/list.html'
    articles = ApprovedArticle.objects.all().filter(status='PUB').annotate(likes_count=Count('liked')).order_by('-updated_at')
    paginate_by = 12
    pages = Paginator(articles, paginate_by)
    queryset = pages.page(page)
    context = {
        'object_list': queryset,
    }
    return render(request, template_name, context)


class ArticleDetailView(DetailView):
    model = ApprovedArticle
    template_name = 'blog/detail.html'
