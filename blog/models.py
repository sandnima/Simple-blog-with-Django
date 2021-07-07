from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils.text import slugify
from profiles.models import Profile

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit
from langdetect import detect
from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField # Uncomment for Ckeditor upload image option


def get_guest_profile():
    pass


class Tag(models.Model):
    tag_name = models.CharField(unique=True, max_length=120)
    
    def __str__(self):
        return f'{self.tag_name}'


def get_default_meta(title, description):
    return Meta.objects.get_or_create(title_tag=title, description_tag=description)[0]
    

class Meta(models.Model):
    title_tag = models.CharField(unique=True, max_length=60)
    description_tag = models.TextField(unique=True, max_length=160)
    
    def __str__(self):
        return f'{self.title_tag}'


def get_main_other_category():
    return MainCategory.objects.get_or_create(name='Other')[0]


class MainCategory(models.Model):
    name = models.CharField(unique=True, max_length=60)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f'{self.name}'


def get_sub_other_category():
    return SubCategory.objects.get_or_create(name='Other')[0]


class SubCategory(models.Model):
    name = models.CharField(unique=True, max_length=60)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(MainCategory, default=get_main_other_category,
                               on_delete=models.SET(get_main_other_category))

    def __str__(self):
        return f'{self.name}'


def get_default_language():
    return Language.objects.get_or_create(name='fa')[0]


class Language(models.Model):
    code = models.CharField(max_length=4,
                            validators=[RegexValidator(regex='^.{2}$', message='Length has to be 2', code='nomatch')],
                            unique=True)

    def save(self, *args, **kwargs):
        self.code = self.code.lower()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.code}'


class Status(models.Model):
    max_length = 3
    DRAFT = 'DFT'
    REQUESTED = 'REQ'
    PENDING = 'PND'
    EDITED = 'EDT'
    PUBLISHED = 'PUB'
    DENIED = 'DEN'
    TRASH = 'TRS'
    STATUS_CHOICES = [
        (DRAFT, 'پیشنویس'),
        (REQUESTED, 'آماده انتشار'),
        (PENDING, 'در دست برسی'),
        (EDITED, 'برسی مجدد'),
        (PUBLISHED, 'منتشر شده'),
        (DENIED, 'رد شده'),
        (TRASH, 'زباله دان'),
    ]


class Article(models.Model):
    title = models.CharField(unique=True, max_length=60)
    slug = models.SlugField(unique=True, max_length=60, allow_unicode=True, blank=True)
    meta = models.OneToOneField(Meta, on_delete=models.PROTECT, blank=True, null=True)
    main_category = models.ForeignKey(MainCategory, default=get_main_other_category,
                                      on_delete=models.PROTECT)
    sub_category = models.ForeignKey(SubCategory,
                                     on_delete=models.PROTECT, blank=True, null=True)
    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    content = RichTextField()
    # content = RichTextUploadingField() # Uncomment for Ckeditor upload image option
    headline = models.TextField(max_length=160)
    lang = models.ForeignKey(Language, on_delete=models.SET(get_default_language), blank=True, null=True)
    image = ProcessedImageField(
        upload_to='banners',
        processors=[ResizeToFit(1024, 1024)],
        format='JPEG',
        options={'quality': 90}
    )
    medium_image = ImageSpecField(
        source='image',
        processors=[ResizeToFit(640, 640)],
        format='JPEG',
        options={'quality': 95}
    )
    small_image = ImageSpecField(
        source='image',
        processors=[ResizeToFit(320, 320)],
        format='JPEG',
        options={'quality': 95}
    )
    tags = models.ManyToManyField(Tag, blank=True)
    liked = models.ManyToManyField(User, blank=True)
    status = models.CharField(max_length=Status.max_length, choices=Status.STATUS_CHOICES,
                              default=Status.DRAFT)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.title}'
    
    def absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title, allow_unicode=True)
        if self.meta is None:
            self.meta = get_default_meta(title=self.title, description=self.headline)
        if self.lang is None:
            code = detect(self.content)
            self.lang = Language.objects.get_or_create(code=code)[0]
        return super().save(*args, **kwargs)
