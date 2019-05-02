from django.urls import path
from django.conf import settings
from django.views import static
from django.views.generic.base import TemplateView
from django.views.generic import RedirectView

from decrypter import views


urlpatterns = [
    path(r'static/<path:path>',
         static.serve, kwargs={'document_root': settings.STATIC_ROOT},
         name='static'),
    path(r'', views.decrypter, name='main'),
    path(r'abc', views.abc, name='abc'),
    path('robots.txt',
        TemplateView.as_view(template_name='robots.txt',
                             content_type='text/plain'),
        name='robots'),
    path('favicon.png', RedirectView.as_view(url='/static/favicon.png'), name='favicon'),
]
