from django import forms
from .models import Article, MetaTag, Category
from ckeditor.fields import RichTextFormField
from mptt.forms import TreeNodeMultipleChoiceField


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=255)
    content = RichTextFormField()
    # categories = TreeNodeMultipleChoiceField(
    #     queryset=Category.objects.all(),
    #     required=False,
    #     )


class MetaModelForm(forms.ModelForm):
    class Meta:
        model = MetaTag
        fields = '__all__'
