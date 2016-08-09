from django.conf.urls import include, url
from django.contrib import admin

from validator.views import validator_service_view

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'matrix_captcha.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^validator-service/$', validator_service_view),
]
