from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader

from .models import ClientIP


def trinity_view(request):
    if request.method == 'POST':
        g_recaptcha_response = request.POST.get('g-recaptcha-response', [])

        if len(g_recaptcha_response) > 0 and g_recaptcha_response[0] != '':
            client_ip = request.META.get('REMOTE_ADDR')
            ClientIP.objects.create(ip_address=client_ip, status='w')
            
            name = request.GET.get('name', '')
            return HttpResponseRedirect('/zion-service/?name={}'.format(name))

    template = loader.get_template('trinity_template.html')
    
    context = {'name': request.GET.get('name', '')}
    return HttpResponse(template.render(context, request))

def zion_view(request):
    name = request.GET.get('name')
    return JsonResponse({"message": "I'm trying to free your mind, {}. But I can only show you the door. You're the one that has to walk through it.".format(name)})

