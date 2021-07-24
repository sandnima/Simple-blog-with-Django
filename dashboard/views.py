from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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


class DashboardIndexView(LoginRequiredMixin, View):
    template_name = 'dashboard/dashboard.html'
    
    def get(self, request):
        context = {
        }
        return render(request, self.template_name, context)


class DashboardArticleListView(LoginRequiredMixin, View):
    template_name = 'dashboard/blog/article_list.html'
    
    def get(self, request, page=1):
        user_profile = Profile.objects.get(user=request.user)
        articles = Article.objects.all().filter(author=user_profile).order_by('-updated_at')
        paginate_by = 10
        pages = Paginator(articles, paginate_by)
        queryset = pages.page(page)
        context = {
            'article_list': queryset,
            'total_pages': pages.num_pages
        }
        return render(request, self.template_name, context)


class DashboardArticleCreateView(LoginRequiredMixin, View):
    template_name = 'dashboard/blog/article_form.html'
    article = None

    def get(self, request):
        form = ArticleUpdateCreateModelForm(instance=self.article)
        context = {
            'form': form,
            'article': self.article,
            'main_category_options': MainCategory.objects.all(),
            'sub_category_options': SubCategory.objects.all(),
            'tag_options': Tag.objects.all(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = ArticleUpdateCreateModelForm(request.POST, request.FILES, instance=self.article)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = Profile.objects.get(user=request.user)
            instance.main_category = form.cleaned_data.get('main_category')
            instance.sub_category = form.cleaned_data.get('sub_category')
            instance.save()
            if not self.article:
                instance.save()
            if request.POST.get('submit') == 'publish':
                if self.article.status in ['DFT', 'PUB', 'EDT']:
                    instance.status = 'PND'
            elif request.POST.get('submit') == 'save':
                instance.status = 'DFT'
            instance.tags.set(form.cleaned_data.get('tags'))
            instance.save()
            return redirect(reverse('dashboard:article_update', kwargs={'slug': instance.slug}))
        else:
            print(form.errors)

        context = {
            'form': form,
            'article': self.article,
            'main_category_options': MainCategory.objects.all(),
            'sub_category_options': SubCategory.objects.all(),
            'tag_options': Tag.objects.all(),
        }
        return render(request, self.template_name, context)


class DashboardArticleUpdateView(DashboardArticleCreateView):
    def get(self, request, slug=None):
        user_profile = Profile.objects.get(user=request.user)
        self.article = get_object_or_404(Article, slug=slug, author=user_profile)
        return super(DashboardArticleUpdateView, self).get(request)

    def post(self, request, slug=None):
        user_profile = Profile.objects.get(user=request.user)
        self.article = get_object_or_404(Article, slug=slug, author=user_profile)
        return super(DashboardArticleUpdateView, self).post(request)
    

@login_required
def article_preview(request, slug):
    template_name = 'dashboard/blog/article_preview.html'
    user_profile = Profile.objects.get(user=request.user)
    article = get_object_or_404(Article, slug=slug)
    if not (article.author == user_profile or request.user.groups.filter(name="ContentModerators").count() > 0):
        raise Http404("Article not found")
    context = {
        'article': article,
    }
    return render(request, template_name, context)


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'dashboard/blog/article_delete.html'
    
    def get_success_url(self):
        return reverse('dashboard:index')
