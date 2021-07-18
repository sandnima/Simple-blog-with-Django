from django.urls import path, register_converter

from .views import IndexView, AboutView
from .converters import UnicodeSlugConverter


register_converter(UnicodeSlugConverter, 'unicode_slug')

app_name = 'home'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
]
