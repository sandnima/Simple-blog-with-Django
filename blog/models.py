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

from mptt.models import MPTTModel, TreeForeignKey
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_delete, post_delete


def get_guest_profile():
    pass


class Tag(models.Model):
    tag_name = models.CharField(unique=True, max_length=120)
    
    def __str__(self):
        return f'{self.tag_name}'


def get_default_meta(title, description=None):
    return MetaTag.objects.get_or_create(title_tag=title, description_tag=description)[0]


class MetaTag(models.Model):
    title_tag = models.CharField(unique=True, max_length=60)
    description_tag = models.TextField(unique=True, max_length=160)
    
    def __str__(self):
        return f'{self.title_tag}'


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
    

def get_default_status():
    return Status.objects.get_or_create(state='پیشنویس')[0]


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


def get_other_category():
    other_meta_title = 'دسته متفرقه'
    other_meta_description = 'این دسته شامل محتوای خارح از دسته بندی های معمولی میشود.'
    meta = get_default_meta(other_meta_title, other_meta_description)
    return Category.objects.get_or_create(name="Other", meta=meta)[0]
    

class Category(MPTTModel):
    name = models.CharField(max_length=120)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            on_delete=models.PROTECT)
    slug = models.SlugField(unique=True, max_length=120, allow_unicode=True, blank=True)
    meta = models.OneToOneField(MetaTag, blank=True, null=True, on_delete=models.PROTECT)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'categories'
        unique_together = ('name', 'parent',)
        
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name, allow_unicode=True)
        if self.meta is None:
            self.meta = get_default_meta(self.name, self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


# Move Category children when parent Category deleted (Not good for SEO)
# If you are using this change parent's on_delete to models.DO_NOTHING

# @receiver(pre_delete, sender=Category, dispatch_uid='delete_category')
# def set_other_category(sender, instance, **kwargs):
#     if instance.name == "Other":
#         if len(instance.get_children()) > 0:
#             for child in instance.get_children():
#                 child.delete()
#     else:
#         parent = instance.get_root() if not instance.is_root_node() else None
#         Category.objects.get_or_create(name="Other", parent=parent)
#         other = Category.objects.get(name="Other", parent=parent)
#         if len(instance.get_children()) > 0:
#             for child in instance.get_children():
#                 child.move_to(other, 'last-child')


class Article(models.Model):
    title = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(unique=True, max_length=255, allow_unicode=True, blank=True)
    meta = models.OneToOneField(MetaTag, blank=True, null=True, on_delete=models.PROTECT)
    category = TreeForeignKey('Category', default=get_other_category, on_delete=models.PROTECT)
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
        if self.slug is None:
            self.slug = slugify(self.title, allow_unicode=True)
        if self.lang is None:
            code = detect(self.content)
            self.lang = Language.objects.get_or_create(code=code)[0]
        if self.meta is None:
            self.meta = get_default_meta(self.title, self.headline)
        return super().save(*args, **kwargs)
