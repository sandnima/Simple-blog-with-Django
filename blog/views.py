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
from profiles.models import Profile
from .forms import ArticleCreateForm
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
def article_create_view(request):
    form = ArticleCreateForm()
    if request.method == "POST":
        form = ArticleCreateForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data['main_category'])
            main_category = MainCategory.objects.get_or_create(name=form.cleaned_data['main_category'])[0]
            sub_category = SubCategory.objects.get_or_create(name=form.cleaned_data['sub_category'])[0]\
                if form.cleaned_data['sub_category'] else None
            profile = Profile.objects.get(user=request.user)
            instance = {
                'title': form.cleaned_data['title'],
                'image': request.FILES['image'],
                'main_category': main_category,
                'sub_category': sub_category,
                'author': profile,
                'content': form.cleaned_data['content'],
                'headline': form.cleaned_data['headline']
            }
            Article.objects.update_or_create(**instance)
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
