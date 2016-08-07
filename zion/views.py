from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.core.cache import cache
import requests

from .models import ClientIP

def call_third_party():
    response = requests.get('https://www.zipcodeapi.com/rest/kpZVAfW18keQsK9j8NGNFiJroM4EFyOZXOVx4SycdN3FxcYG0FtGXc7mZb0FKPFH/info.json/90210/degrees')
    return HttpResponse(response)

def trinity_view(request):
    client_ip = request.META.get('REMOTE_ADDR')
    matched_ips = cache.keys('{}_status'.format(client_ip))

    if len(matched_ips) > 0:
        if cache.get('{}_status'.format(client_ip)) == 'w':
            return call_third_party()
        else:
            return JsonResponse({'detail': 'Permission Denied.'})
    else:
        g_recaptcha_response = request.POST.get('g-recaptcha-response', [])

        if len(g_recaptcha_response) > 0 and g_recaptcha_response[0] != '':

            cache.set('{}_status'.format(client_ip), 'w')
            return call_third_party()
        else:
            template = loader.get_template('trinity_template.html')
            context = {'name': request.GET.get('name', '')}
            return HttpResponse(template.render(context, request))
