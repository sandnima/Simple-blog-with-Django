from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from profiles.models import Profile

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit
from langdetect import detect
from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField # Uncomment for Ckeditor upload image option


class Tag(models.Model):
    tag_name = models.CharField(unique=True, max_length=120)
    
    def __str__(self):
        return f'{self.tag_name}'


class Meta(models.Model):
    title_tag = models.CharField(unique=True, max_length=60)
    description_tag = models.TextField(unique=True, max_length=160)
    
    def __str__(self):
        return f'{self.title_tag}'


class Category(models.Model):
    name = models.CharField(unique=True, max_length=120)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f'{self.name}'


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
    PENDING = 'PND'
    EDITED = 'EDT'
    PUBLISHED = 'PUB'
    DENIED = 'DEN'
    TRASH = 'TRS'
    STATUS_CHOICES = [
        (DRAFT, 'پیشنویس'),
        (PENDING, 'در دست برسی'),
        (EDITED, 'برسی مجدد'),
        (PUBLISHED, 'منتشر شده'),
        (DENIED, 'رد شده'),
        (TRASH, 'زباله دان'),
    ]


def get_other_category():
    return Category.objects.get_or_create(name='Other')[0]


def get_guest_profile():
    pass


def get_default_language():
    return Language.objects.get_or_create(name='fa')[0]


def get_default_status():
    return Status.objects.get_or_create(state='پیشنویس')[0]


class Article(models.Model):
    title = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(unique=True, max_length=255, allow_unicode=True)
    meta = models.OneToOneField(Meta, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, default=get_other_category, on_delete=models.SET(get_other_category))
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
        return reverse("blog:detail", kwargs={"pk": self.pk})
    
    def save(self, *args, **kwargs):
        if self.lang is None:
            code = detect(self.content)
            self.lang = Language.objects.get_or_create(code=code)[0]
        return super().save(*args, **kwargs)
    
    

