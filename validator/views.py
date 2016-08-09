from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.core.cache import cache
import requests

def call_third_party():
    # response = requests.get('https://www.zipcodeapi.com/rest/kwMXRk9wskTIzAY7mA2cB6HJbKHYurxPXjMPEVm6ffPPPNXboZoZ65JhPqfkSM9Q/info.json/90210/degrees')
    # return JsonResponse(response.json())
    response = requests.get('https://www.zipcodeapi.com/rest/kwMXRk9wskTIzAY7mA2cB6HJbKHYurxPXjMPEVm6ffPPPNXboZoZ65JhPqfkSM9Q/info.xml/90210/degrees', headers={'Content-Type': 'text/xml'})
    return HttpResponse(response.content)

def validator_service_view(request):
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
            template = loader.get_template('validator_template.html')
            context = {'name': request.GET.get('name', '')}
            return HttpResponse(template.render(context, request))
