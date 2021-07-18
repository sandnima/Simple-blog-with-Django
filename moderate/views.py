from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .decorators import user_in_group
from django.urls import resolve, reverse

from blog.models import Article


@login_required
@user_in_group(group="ContentModerators")
def moderate(request):
    template_name = 'moderate/moderate.html'
    context = {
    }
    return render(request, template_name, context)


@login_required
@user_in_group(group="ContentModerators")
def article_list(request, page=1):
    template_name = 'moderate/blog/article_list.html'
    # user_profile = Profile.objects.get(user=request.user)
    articles = Article.objects.all().exclude(status='DFT').order_by('-updated_at')
    paginate_by = 10
    pages = Paginator(articles, paginate_by)
    queryset = pages.page(page)
    context = {
        'object_list': queryset,
        'total_pages': pages.num_pages
    }
    return render(request, template_name, context)
