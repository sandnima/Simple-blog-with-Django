from django import forms
from .models import Article, Meta


class ArticleModelForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        
        
class MetaModelForm(forms.ModelForm):
    class Meta:
        model = Meta
        fields = '__all__'
