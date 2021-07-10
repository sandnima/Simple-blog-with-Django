from django import forms
from .models import Article, MainCategory, SubCategory, Tag, Meta
from ckeditor.fields import RichTextFormField


class ArticleUpdateCreateModelForm(forms.ModelForm):
    # title = forms.CharField(
    #     max_length=60,
    #     widget=forms.TextInput(
    #         attrs={
    #             'dir': 'auto',
    #             'class': 'form-control form-control-lg mb-3',
    #             'placeholder': 'Title',
    #             'aria-label': 'Title',
    #         },
    #     ),
    # )
    # image = forms.ImageField()
    # content = RichTextFormField()
    # headline = forms.CharField(
    #     max_length=160,
    #     widget=forms.Textarea(
    #         attrs={
    #             'dir': 'auto',
    #             'class': 'form-control',
    #             'style': 'height: 100px;',
    #         },
    #     ),
    # )
    # main_category = forms.CharField(
    #     max_length=60,
    #     widget=forms.TextInput(
    #         attrs={
    #             'dir': 'auto',
    #             'class': 'form-control mb-2',
    #             'list': 'main_category_options',
    #             'placeholder': 'Main Category',
    #         },
    #     ),
    # )
    # sub_category = forms.CharField(
    #     max_length=60,
    #     required=False,
    #     widget=forms.TextInput(
    #         attrs={
    #             'dir': 'auto',
    #             'class': 'form-control mb-3',
    #             'list': 'sub_category_options',
    #             'placeholder': 'Sub Category',
    #         },
    #     ),
    # )
    # tags = forms.CharField(
    #     max_length=255,
    #     widget=forms.TextInput(
    #         attrs={
    #             'dir': 'auto',
    #             'class': 'form-control mb-3 tagin',
    #             'list': 'sub_category_options',
    #             'placeholder': 'Sub Category',
    #             'data-separator': '" "'
    #         },
    #     ),
    # )

    def __init__(self, *args, **kwargs):
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
    # image = forms.ImageField(
    #     widget=forms.ClearableFileInput(
    #         attrs={
    #             'class': 'form-control mb-3',
    #             'onchange': "readURL(this)",
    #             'accept': "image/png, image/jpeg",
    #         },
    #     )
    # )
    
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
        return MainCategory.objects.get_or_create(name=self.cleaned_data['main_category'].capitalize())[0]
    
    def clean_sub_category(self):
        if self.cleaned_data['sub_category']:
            return SubCategory.objects.get_or_create(name=self.cleaned_data['sub_category'].capitalize(),
                                                     parent=self.cleaned_data['main_category'].capitalize())[0]
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
    
    # def clean_main_category(self):
    #     main_category_passed = self.cleaned_data.get("main_category")
    #     return MainCategory.objects.get_or_create(main_category_passed)[0]


class MetaModelForm(forms.ModelForm):
    class Meta:
        model = Meta
        fields = '__all__'
