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
    template_name = 'blog/list.html'
    queryset = Article.objects.all()


class ArticleDetailView(DetailView):
    template_name = 'blog/detail.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Article, id=id_)


class ArticleCreateView(CreateView):
    template_name = 'blog/create.html'
    form_class = ArticleModelForm
    
    # success_url = '/'
    def form_valid(self, form):
        return super().form_valid(form)
    
    # def get_success_url(self):
    #     return '/'


class ArticleUpdateView(UpdateView):
    template_name = 'blog/create.html'
    form_class = ArticleModelForm
    
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Article, id=id_)
    
    # success_url = '/'
    def form_valid(self, form):
        return super().form_valid(form)
    
    # def get_success_url(self):
    #     return '/'


class ArticleDeleteView(DeleteView):
    template_name = 'blog/delete.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Article, id=id_)
    
    def get_success_url(self):
        return reverse('blog:list')

'''
def list_view(request):
    context = {
        'objects': Article.objects.all()
    }
    return render(request, "blog/list.html", context)


def detail_view(request, id):
    context = {
        'object': get_object_or_404(Article, id=id)
    }
    return render(request, "blog/detail.html", context)
'''
