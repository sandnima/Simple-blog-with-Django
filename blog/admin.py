from django.contrib import admin
from .models import Article, Meta, Category


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published')
    list_filter = ('published',)
    prepopulated_fields = {'slug': ('title',)}
    

class MetaAdmin(admin.ModelAdmin):
    list_display = ('title_tag', 'description_tag')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Meta, MetaAdmin)
admin.site.register(Category)

