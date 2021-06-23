from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'active')
    list_filter = ('active',)


admin.site.register(Article, ArticleAdmin)
