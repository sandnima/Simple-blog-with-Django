from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import resolve, reverse
from django.db.models import Count
from .decorators import user_in_group

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
    get_main_other_category,
    get_sub_other_category
)
from profiles.models import Profile

# import forms
from .forms import ArticleUpdateCreateModelForm


@login_required
# @user_in_group(group="")
def dashboard(request):
    template_name = 'dashboard/dashboard.html'
    context = {
    }
    return render(request, template_name, context)


@login_required
def article_list(request, page=1):
    template_name = 'dashboard/article_list.html'
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
    template_name = 'dashboard/article_create_update.html'
    user_profile = Profile.objects.get(user=request.user)
    article = get_object_or_404(Article, slug=slug, author=user_profile) if slug else None
    form = ArticleUpdateCreateModelForm(request.POST or None, request.FILES or None, instance=article)
    if request.method == "POST":
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = user_profile
            instance.main_category = form.cleaned_data['main_category']
            instance.sub_category = form.cleaned_data['sub_category']
            print(form.cleaned_data['headline'])
            instance.save()
            instance.tags.set(form.cleaned_data['tags'])
            return redirect(reverse('dashboard:update', kwargs={'slug': instance.slug}))
            # if resolve(request.path).url_name == "create":
            #     return redirect(reverse('dashboard:update', kwargs={'slug': instance.slug}))
            # form = ArticleUpdateCreateModelForm(instance=instance)
        else:
            print(form.errors)
    
    get_main_other_category()
    context = {
        'form': form,
        'main_category_options': MainCategory.objects.all(),
        'sub_category_options': SubCategory.objects.all(),
        'tag_options': Tag.objects.all(),
    }
    return render(request, template_name, context)


@login_required
def article_preview(request, slug):
    template_name = 'dashboard/article_preview.html'
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
    template_name = 'dashboard/delete.html'
    
    def get_success_url(self):
        return reverse('dashboard:index')
