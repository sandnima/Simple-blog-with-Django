from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='banners')

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"id": self.id})
