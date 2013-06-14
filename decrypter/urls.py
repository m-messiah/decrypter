from django.conf.urls import patterns, include, url
from django.conf import settings
import views

urlpatterns = patterns(
    '',
    url(r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
    url(r'^$', views.decrypter),
)
