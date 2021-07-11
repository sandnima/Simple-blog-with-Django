from django import forms
from .models import Article, MainCategory, SubCategory, Tag, Meta
from ckeditor.fields import RichTextFormField


class CustomFileInput(forms.FileInput):
    pass


class ArticleUpdateCreateModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if kwargs['instance']:
            instance = kwargs['instance']
            updated_initial = dict()
            updated_initial['main_category'] = instance.main_category
            updated_initial['sub_category'] = instance.sub_category
            updated_initial['tags'] = ""
            for tag in instance.tags.all():
                updated_initial['tags'] += "#"+str(tag).upper()+" "
            kwargs.update(initial=updated_initial)
        super(ArticleUpdateCreateModelForm, self).__init__(*args, **kwargs)
    
    main_category = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={
                'dir': 'auto',
                'class': 'form-control mb-2',
                'list': 'main_category_options',
                'placeholder': 'Main Category',
            },
        ),
    )
    sub_category = forms.CharField(
        max_length=60,
        required=False,
        widget=forms.TextInput(
            attrs={
                'dir': 'auto',
                'class': 'form-control mb-3',
                'list': 'sub_category_options',
                'placeholder': 'Sub Category',
            },
        ),
    )
    tags = forms.CharField(
        max_length=60,
        required=False,
        widget=forms.TextInput(
            attrs={
                'dir': 'auto',
                'class': 'form-control mb-3 tagin',
                'placeholder': 'Tags',
                'data-separator': ' ',
            },
        ),
    )
    image = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control mb-3 d-none',
                'onchange': "readURL(this)",
                'accept': "image/png, image/jpeg",
            },
        )
    )
    
    class Meta:
        model = Article
        fields = ('title', 'image', 'content', 'headline',)
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'dir': 'auto',
                    'class': 'form-control form-control-lg mb-2',
                    'placeholder': 'Title',
                    'aria-label': 'Title',
                },
            ),
            'content': RichTextFormField(),
            'headline': forms.Textarea(
                attrs={
                    'dir': 'auto',
                    'class': 'form-control',
                    'style': 'height: auto;',
                },
            ),
        }
        
    def clean_main_category(self):
        return MainCategory.objects.get_or_create(name=str(self.cleaned_data['main_category']).capitalize())[0]
    
    def clean_sub_category(self):
        if self.cleaned_data['sub_category']:
            return SubCategory.objects.get_or_create(name=str(self.cleaned_data['sub_category']).capitalize(),
                                                     parent=self.cleaned_data['main_category'])[0]
        else:
            return None
    
    def clean_tags(self):
        tags = self.cleaned_data['tags']
        tags_list = []
        for tag in tags.split():
            tag = tag.strip("#")
            if len(tag) > 0:
                tags_list.append(Tag.objects.get_or_create(tag_name=tag.upper())[0])
        return tags_list


class MetaModelForm(forms.ModelForm):
    class Meta:
        model = Meta
        fields = '__all__'
