from django import forms
from .models import Article, MainCategory, Meta
from ckeditor.fields import RichTextFormField


class ArticleModelForm(forms.Form):
    title = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': 'Title',
                'aria-label': 'Title',
            },
        ),
    )
    content = RichTextFormField(max_length=2048)
    headline = forms.CharField(
        max_length=160,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'style': 'height: 100px;'
            }
        ),
    )
    main_category = forms.CharField(max_length=60)
    sub_category = forms.CharField(max_length=60)
    
        
class MetaModelForm(forms.ModelForm):
    class Meta:
        model = Meta
        fields = '__all__'
