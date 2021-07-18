from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import resolve, reverse
from django.db.models import Count

# import models
from django.views.generic import (
    DetailView,
    DeleteView,
)
from blog.models import (
    Article,
    MainCategory,
    SubCategory,
    Tag,
)
from profiles.models import Profile

# import forms
from .forms import ArticleUpdateCreateModelForm


@login_required
def dashboard(request):
    template_name = 'dashboard/dashboard.html'
    context = {
    }
    return render(request, template_name, context)


@login_required
def article_list(request, page=1):
    template_name = 'dashboard/blog/article_list.html'
    user_profile = Profile.objects.get(user=request.user)
    articles = Article.objects.all().filter(author=user_profile).order_by('-updated_at')
    paginate_by = 10
    pages = Paginator(articles, paginate_by)
    queryset = pages.page(page)
    context = {
        'object_list': queryset,
        'total_pages': pages.num_pages
    }
    return render(request, template_name, context)


@login_required
def article_update_or_create(request, slug=None):
    template_name = 'dashboard/blog/article_create_update.html'
    user_profile = Profile.objects.get(user=request.user)
    article = get_object_or_404(Article, slug=slug, author=user_profile) if slug else None
    form = ArticleUpdateCreateModelForm(request.POST or None, request.FILES or None, instance=article)
    if request.method == "POST":
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = user_profile
            instance.main_category = form.cleaned_data.get('main_category')
            instance.sub_category = form.cleaned_data.get('sub_category')
            if not article:
                instance.save()
            if request.POST.get('submit') == 'publish':
                if article.status in ['DFT', 'PUB', 'EDT']:
                    instance.status = 'PND'
            elif request.POST.get('submit') == 'save':
                instance.status = 'DFT'
            instance.tags.set(form.cleaned_data.get('tags'))
            instance.save()
            return redirect(reverse('dashboard:update', kwargs={'slug': instance.slug}))
        else:
            print(form.errors)
    
    context = {
        'form': form,
        'article': article if article else None,
        'main_category_options': MainCategory.objects.all(),
        'sub_category_options': SubCategory.objects.all(),
        'tag_options': Tag.objects.all(),
    }
    return render(request, template_name, context)


@login_required
def article_preview(request, slug):
    template_name = 'dashboard/blog/article_preview.html'
    user_profile = Profile.objects.get(user=request.user)
    article = get_object_or_404(Article, slug=slug)
    if not (article.author == user_profile or request.user.groups.filter(name="ContentModerators").count() > 0):
        raise Http404("Article not found")
    context = {
        'object': article,
    }
    return render(request, template_name, context)


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'dashboard/blog/article_delete.html'
    
    def get_success_url(self):
        return reverse('dashboard:index')
