from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.conf import settings
import requests


def check_captcha(captcha_response, remote_ip):
    post_data = {
        "secret": settings.RECAPTCHA_SECRETKEY,
        "response": captcha_response,
        "remoteip": remote_ip
    }

    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=post_data)
    if response.json()['success'] == True:
        return True
    return False

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
        if g_recaptcha_response != '' and check_captcha(g_recaptcha_response, client_ip):
            cache.set('{}_status'.format(client_ip), 'w')
            return call_third_party(method, data)

        else:
            unathorised_request_num = cache.get_or_set('{}_unathorised_request_num'.format(client_ip), 0)
            if unathorised_request_num < settings.MAX_UNATHORISED_REQUEST_NUM:
                cache.incr('{}_unathorised_request_num'.format(client_ip))
                template = loader.get_template('ticket_template.html')

                context = {
                    'site_key': settings.RECAPTCHA_SITEKEY,
                    'data': data
                }
                return HttpResponse(template.render(context, request))
            return HttpResponse('You are not allowed to access this service anymore.')
