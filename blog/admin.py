from django.contrib import admin
from .models import (
    MainCategory,
    SubCategory,
    Language,
    Tag,
    Article,
    ApprovedArticle,
)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'status')
    list_filter = ('status', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    

class MetaAdmin(admin.ModelAdmin):
    list_display = ('title_tag', 'description_tag')


admin.site.register(Article, ArticleAdmin)
admin.site.register(ApprovedArticle, ArticleAdmin)
admin.site.register(MainCategory)
admin.site.register(SubCategory)
admin.site.register(Language)
admin.site.register(Tag)

