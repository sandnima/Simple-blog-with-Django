from django.db import models
from django.urls import reverse_lazy
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils.text import slugify
from profiles.models import Profile

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit
from langdetect import detect, LangDetectException


def get_guest_profile(**kwargs):
    pass


class Tag(models.Model):
    tag_name = models.CharField(unique=True, max_length=120)
    
    def __str__(self):
        return f'{self.tag_name}'


def get_main_other_category(**kwargs):
    return MainCategory.objects.get_or_create(name='Other')[0]


class MainCategory(models.Model):
    name = models.CharField(unique=True, max_length=60)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f'{self.name}'


def get_sub_other_category(**kwargs):
    return SubCategory.objects.get_or_create(name='Other')[0]


class SubCategory(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(MainCategory, default=get_main_other_category,
                               on_delete=models.SET(get_main_other_category))
    
    class Meta:
        unique_together = ('name', 'parent',)

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
    TRASH = 'TSH'
    STATUS_CHOICES = [
        (DRAFT, 'پیشنویس'),
        (REQUESTED, 'آماده انتشار'),
        (PENDING, 'در دست برسی'),
        (EDITED, 'تغییر یافته'),
        (PUBLISHED, 'منتشر شده'),
        (DENIED, 'رد شده'),
        (TRASH, 'زباله دان'),
    ]
    

class AbstractArticle(models.Model):
    DEFAULT_BANNER = 'banners/placeholder-banner.png'
    
    title = models.CharField(unique=True, max_length=60)
    slug = models.SlugField(unique=True, max_length=60, allow_unicode=True, blank=True)
    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    content = models.TextField(blank=True, null=True)
    headline = models.TextField(max_length=160, blank=True, null=True)
    meta_title = models.CharField(unique=True, blank=True, max_length=60)
    meta_description = models.TextField(unique=True, blank=True, max_length=160)
    main_category = models.ForeignKey(MainCategory, default=get_main_other_category,
                                      on_delete=models.PROTECT, blank=True)
    sub_category = models.ForeignKey(SubCategory,
                                     on_delete=models.PROTECT, blank=True, null=True)
    image = ProcessedImageField(
        upload_to='banners',
        processors=[ResizeToFit(1024, 1024)],
        format='JPEG',
        options={'quality': 90},
        blank=True,
        null=True,
        default=DEFAULT_BANNER
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
    lang = models.ForeignKey(Language, on_delete=models.SET(get_default_language), blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.CharField(max_length=Status.max_length, choices=Status.STATUS_CHOICES,
                              default=Status.DRAFT)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.title}'
    
    def absolute_url(self):
        return reverse_lazy("blog:detail", kwargs={"slug": self.slug})
    
    def update_url(self):
        return reverse_lazy("dashboard:article_update", kwargs={"slug": self.slug})
    
    def preview_url(self):
        return reverse_lazy("dashboard:article_preview", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        if self.slug is (None or ""):
            self.slug = slugify(self.title, allow_unicode=True)
        if self.meta_title is None or self.meta_title == "":
            self.meta_title = self.title
        if self.meta_description is None or self.meta_description == "":
            self.meta_description = self.meta_title
        if self.lang is None:
            try:
                code = detect(self.content)
            except LangDetectException:
                code = 'fa'
            self.lang = Language.objects.get_or_create(code=code)[0]
        return super().save(*args, **kwargs)
    
    class Meta:
        abstract = True


def get_or_create_meta(class_, title, description):
    return class_.objects.get_or_create(title_tag=title, description_tag=description)[0]


class Article(AbstractArticle):
    pass
    

class ApprovedArticle(AbstractArticle):
    content = models.TextField(blank=False, null=False)
    image = ProcessedImageField(
        upload_to='banners',
        processors=[ResizeToFit(1024, 1024)],
        format='JPEG',
        options={'quality': 90},
        blank=False,
        null=False,
        default="banners/banner.jpg"
    )
    headline = models.TextField(max_length=160, blank=False, null=False)
    meta_description = models.TextField(unique=True, max_length=160)
    liked = models.ManyToManyField(User, blank=True)
    origin = models.OneToOneField(Article, on_delete=models.PROTECT)
    approver = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='approver')
    
    def approve_article(self):
        self.title = self.origin.title
        self.slug = self.origin.slug
        self.meta.approve_meta(self.origin.meta)
        self.main_category = self.origin.main_category
        self.sub_category = self.origin.sub_category
        self.author = self.origin.author
        self.content = self.origin.content
        self.headline = self.origin.headline
        self.lang = self.origin.lang
        self.image = self.origin.image
        self.medium_image = self.origin.medium_image
        self.small_image = self.origin.small_image
        self.tags.set(self.origin.tags.all())
        self.save()
        return self
