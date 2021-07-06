from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import (
    DetailView,
    UpdateView,
    DeleteView,
)
from .models import (
    Article,
    MainCategory,
    SubCategory,
    get_main_other_category,
    get_sub_other_category
)
from .forms import ArticleModelForm
from django.urls import reverse


def article_list(request, page=1):
    template_name = 'blog/list.html'
    articles = Article.objects.all().filter(status='PUB').annotate(likes_count=Count('liked')).order_by('-updated_at')
    paginate_by = 1
    pages = Paginator(articles, paginate_by)
    queryset = pages.page(page)
    context = {
        'object_list': queryset,
    }
    return render(request, template_name, context)


# class ArticleListView(ListView):
#     template_name = 'blog/list.html'
#     # paginate_by = 9
#     queryset = Article.objects.all().filter(status='PUB').annotate(likes_count=Count('liked')).order_by('-updated_at')


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/detail.html'


@login_required
def article_create_view(request):
    template_name = 'blog/create.html'
    form_class = ArticleModelForm
    get_main_other_category()
    get_sub_other_category()
    context = {
        'form': form_class,
        'main_category_options': MainCategory.objects.all(),
        'sub_category_options': SubCategory.objects.all()
    }
    return render(request, template_name, context)


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
