from django.shortcuts import render, get_object_or_404
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
    get_main_other_category,
    get_sub_other_category
)
from profiles.models import Profile

# import forms
from .forms import ArticleUpdateCreateModelForm


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
    }
    return render(request, template_name, context)


@login_required
def article_update_or_create_view(request, slug=None):
    if resolve(request.path).url_name:
        pass
    article = get_object_or_404(Article, slug=slug) if slug else None
    form = ArticleUpdateCreateModelForm(request.POST or None, request.FILES or None, instance=article)
    if request.method == "POST":
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = Profile.objects.get(user=request.user)
            instance.main_category = form.cleaned_data['main_category']
            instance.sub_category = form.cleaned_data['sub_category']
            instance.tags.set(form.cleaned_data['tags'])
            instance.save()
            form = ArticleUpdateCreateModelForm(instance=instance)
        else:
            print(form.errors)
    
    template_name = 'dashboard/create_update.html'
    
    get_main_other_category()
    get_sub_other_category()
    context = {
        'form': form,
        'main_category_options': MainCategory.objects.all(),
        'sub_category_options': SubCategory.objects.all(),
        'tag_options': Tag.objects.all(),
    }
    return render(request, template_name, context)


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'dashboard/delete.html'
    
    def get_success_url(self):
        return reverse('dashboard:index')
