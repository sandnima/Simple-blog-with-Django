from django import forms
from .models import Article, MainCategory, Meta
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
    
    class Meta:
        model = Article
        fields = ('title', 'image', 'content', 'headline', 'tags')
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'dir': 'auto',
                    'class': 'form-control form-control-lg mb-3',
                    'placeholder': 'Title',
                    'aria-label': 'Title',
                },
            ),
            'content': RichTextFormField(),
            'headline': forms.Textarea(
                attrs={
                    'dir': 'auto',
                    'class': 'form-control',
                    'style': 'height: 100px;',
                },
            ),
            'tags': forms.TextInput(
                attrs={
                    'dir': 'auto',
                    'class': 'form-control mb-3 tagin',
                    'list': 'sub_category_options',
                    'placeholder': 'Sub Category',
                    'data-separator': '" "'
                },
            ),
        }
    
    # def clean_main_category(self):
    #     main_category_passed = self.cleaned_data.get("main_category")
    #     return MainCategory.objects.get_or_create(main_category_passed)[0]


class MetaModelForm(forms.ModelForm):
    class Meta:
        model = Meta
        fields = '__all__'
