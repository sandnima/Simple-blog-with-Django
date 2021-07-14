from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_groups(**kwargs):
    from django.contrib.auth.models import Group
    Group.objects.get_or_create(name="ContentModerators")


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    
    def ready(self):
        post_migrate.connect(create_groups, sender=self)
