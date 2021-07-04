from django import forms
from .models import Article, Meta


class ArticleModelForm(forms.Form):
    title = forms.CharField(max_length=255)
        
        
class MetaModelForm(forms.ModelForm):
    class Meta:
        model = Meta
        fields = '__all__'
