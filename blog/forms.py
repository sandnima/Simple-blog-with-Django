from django import forms
from .models import Article, MainCategory, Meta
from ckeditor.fields import RichTextFormField


class ArticleModelForm(forms.Form):
    title = forms.CharField(max_length=60)
    content = RichTextFormField(max_length=2048)
    main_category = forms.CharField(max_length=60)
    sub_category = forms.CharField(max_length=60)
    
        
class MetaModelForm(forms.ModelForm):
    class Meta:
        model = Meta
        fields = '__all__'
