from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from views import main_page, get_post

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^$', main_page),
    url(r'^post/([0-9]{1,5})', get_post),
)
