from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^$', views.main_page),
    url(r'^post/([0-9]{1,5})', views.get_post),
    url(r'^generate/$', views.generate),
)
