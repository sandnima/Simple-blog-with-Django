from django.contrib import admin
from .models import Article, MetaTag, Language, Tag, Category

from mptt.admin import DraggableMPTTAdmin


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'status')
    list_filter = ('status', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    

class CategoryAdmin(DraggableMPTTAdmin):
    prepopulated_fields = {'slug': ('name',)}
    

class MetaAdmin(admin.ModelAdmin):
    list_display = ('title_tag', 'description_tag')


admin.site.register(Article, ArticleAdmin)
admin.site.register(MetaTag, MetaAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Language)
admin.site.register(Tag)

