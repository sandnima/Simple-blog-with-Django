from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)
from .models import Article
from .forms import ArticleModelForm
from django.urls import reverse


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/list.html'
    # queryset = Article.objects.all()


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/detail.html'


class ArticleCreateView(CreateView):
    template_name = 'blog/create.html'
    form_class = ArticleModelForm
    
    # success_url = '/'
    # def form_valid(self, form):
    #     return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'blog/create.html'
    form_class = ArticleModelForm
    
    # success_url = '/'
    def form_valid(self, form):
        return super().form_valid(form)
    
    # def get_success_url(self):
    #     return '/'


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'blog/delete.html'
    
    def get_success_url(self):
        return reverse('blog:list')
