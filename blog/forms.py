from django import forms
from .models import Article, MainCategory, Meta
from ckeditor.fields import RichTextFormField


class ArticleModelForm(forms.Form):
    title = forms.CharField(max_length=255)
    content = RichTextFormField()
    main_category = forms.CharField(max_length=120)
    sub_category = forms.CharField(max_length=120)
    
        
class MetaModelForm(forms.ModelForm):
    class Meta:
        model = Meta
        fields = '__all__'
