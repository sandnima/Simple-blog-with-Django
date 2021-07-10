from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import resolve
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
from profiles.models import Profile
from .forms import ArticleUpdateCreateModelForm
from django.urls import reverse


def article_list(request, page=1):
    template_name = 'blog/list.html'
    articles = Article.objects.all().filter(status='PUB').annotate(likes_count=Count('liked')).order_by('-updated_at')
    paginate_by = 12
    pages = Paginator(articles, paginate_by)
    queryset = pages.page(page)
    context = {
        'object_list': queryset,
    }
    return render(request, template_name, context)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/detail.html'


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
        else:
            print(form.errors)
        
    template_name = 'blog/create.html'
    
    get_main_other_category()
    get_sub_other_category()
    context = {
        'form': form,
        'main_category_options': MainCategory.objects.all(),
        'sub_category_options': SubCategory.objects.all()
    }
    return render(request, template_name, context)


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'blog/create.html'
    form_class = ""
    
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
