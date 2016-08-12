from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.conf import settings
import requests


def build_soap_request_body(data):
    data_string = ""
    for key, value in data.items():
        new_key_value_part = ''
        data_string = "{}<{}>{}</{}>".format(data_string, key, value, key)
    return '<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://my.org/ns/"><SOAP-ENV:Body><ns1:booking>{}</ns1:booking></SOAP-ENV:Body></SOAP-ENV:Envelope>'.format(data_string)


def call_third_party(method, data):
    headers = {'Content-Type': 'text/xml'}
    url = settings.BACKEND_URL
    request_body = build_soap_request_body(data)

    response = requests.post(url, data=request_body, headers=headers)

    return HttpResponse(response.content)


@csrf_exempt
def ticket_service_view(request):
    if request.method == 'POST':
        method, data = 'post', request.POST
    else:
        method, data = 'get', request.GET

    client_ip = request.META.get('REMOTE_ADDR')
    matched_ips = cache.keys('{}_status'.format(client_ip))

    if len(matched_ips) > 0:
        if cache.get('{}_status'.format(client_ip)) == 'w':
            return call_third_party(method, data)
        else:
            return JsonResponse({'detail': 'Permission Denied.'})

    else:
        g_recaptcha_response = request.POST.get('g-recaptcha-response', [])

        if len(g_recaptcha_response) > 0 and g_recaptcha_response[0] != '':
            cache.set('{}_status'.format(client_ip), 'w')
            return HttpResponse('You are allowed to call the service now.')

        else:
            template = loader.get_template('ticket_template.html')
            context = {'site_key': settings.RECAPTCHA_SITEKEY}
            return HttpResponse(template.render(context, request))
