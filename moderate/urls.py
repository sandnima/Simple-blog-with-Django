from django.urls import path
from .views import (
    moderate
)

app_name = 'moderate'
urlpatterns = [
    path('', moderate, name='index'),
]
