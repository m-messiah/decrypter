from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
import views
from mezzanine.core.views import direct_to_template

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r"^$", direct_to_template, {"template": "index.html"}, name="home"),
    ('^', include("mezzanine.urls")),
)

handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
