from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from profiles.models import Profile

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit
from langdetect import detect


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
    code = models.CharField(max_length=4, validators=[RegexValidator(regex='^.{2}$', message='Length has to be 2', code='nomatch')], unique=True)

    def save(self, *args, **kwargs):
        self.code = self.code.lower()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.code}'


def get_other_category():
    return Category.objects.get_or_create(name='Other')[0]


def get_default_language():
    return Language.objects.get_or_create(name='fa')[0]


class Article(models.Model):
    title = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(unique=True, max_length=255, allow_unicode=True)
    meta = models.OneToOneField(Meta, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.SET(get_other_category))
    content = models.TextField()
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
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    liked = models.ManyToManyField(User, blank=True)
    published = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def headline(self):
        return self.content[:160]
    
    def __str__(self):
        return f'{self.title}'
    
    def absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.pk})
    
    def save(self, *args, **kwargs):
        if self.lang is None:
            code = detect(self.content)
            self.lang = Language.objects.get_or_create(code=code)[0]
        return super().save(*args, **kwargs)
    
    

