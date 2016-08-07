from django.conf.urls import include, url
from django.contrib import admin

from zion.views import trinity_view, zion_view

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'matrix_captcha.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^zion-service/$', zion_view),
    url(r'^trinity-service/$', trinity_view),
]

