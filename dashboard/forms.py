from django import forms
from blog.models import Article, MainCategory, SubCategory, Tag
from ckeditor.fields import RichTextFormField


class ArticleUpdateCreateModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if kwargs['instance']:
            instance = kwargs['instance']
            updated_initial = dict()
            updated_initial['main_category'] = instance.main_category
            updated_initial['sub_category'] = instance.sub_category
            updated_initial['tags'] = ""
            for tag in instance.tags.all():
                updated_initial['tags'] += "#" + str(tag).upper() + " "
            kwargs.update(initial=updated_initial)
        super(ArticleUpdateCreateModelForm, self).__init__(*args, **kwargs)
    
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control mb-3 d-none',
                'tabindex': '-1',
                'onchange': "readURL(this)",
                'accept': "image/png, image/jpeg",
            },
        )
    )
    main_category = forms.CharField(
        required=False,
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
        required=False,
        max_length=60,
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
        required=False,
        max_length=60,
        widget=forms.TextInput(
            attrs={
                'dir': 'auto',
                'class': 'form-control mb-3 tagin',
                'placeholder': 'Tags',
                'data-separator': ' ',
            },
        ),
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
                    'required': False,
                    'class': 'form-control',
                    'style': 'height: auto;',
                },
            ),
        }

    def clean_headline(self):
        if self.cleaned_data['headline'] is None or self.cleaned_data['headline'] == "":
            return f"Short headline for Article: {self.cleaned_data['title']}"
        
    def clean_main_category(self):
        if self.cleaned_data['main_category'] is None:
            return None
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
