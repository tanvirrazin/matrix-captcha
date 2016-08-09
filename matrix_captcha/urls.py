from django.conf.urls import include, url
from django.contrib import admin

from ticket.views import ticket_service_view

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'matrix_captcha.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ticket-service/$', ticket_service_view),
]
