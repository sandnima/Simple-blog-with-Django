from django.contrib import admin
from django.urls import path, include  # add re_path for Ckeditor upload image option
from django.conf.urls.static import static
from django.conf import settings

from .views import AboutView, IndexView


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('accounts/', include('allauth.urls'), name='accounts'),
    # re_path(r'^ckeditor/', include('ckeditor_uploader.urls')), # Uncomment for Ckeditor upload image option
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('blog/', include('blog.urls', namespace='blog')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('moderate/', include('moderate.urls', namespace='moderate')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
