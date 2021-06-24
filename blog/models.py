from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import Profile


class Meta(models.Model):
    title_tag = models.CharField(max_length=60)
    description_tag = models.CharField(max_length=160)
    
    def __str__(self):
        return f'{self.title_tag}'


class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    meta = models.OneToOneField(
        Meta,
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    image = models.ImageField(upload_to='banners')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    liked = models.ManyToManyField(User, blank=True)
    published = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"id": self.id})
    
    def __str__(self):
        return f'{self.title}'
