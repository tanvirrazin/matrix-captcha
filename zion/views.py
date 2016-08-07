from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

def trinity_view(request):
    if request.method == 'POST':
        print request.POST
    else:
        pass

    template = loader.get_template('trinity_template.html')
    
    context = {}
    return HttpResponse(template.render(context, request))

def zion_view(request):
    name = request.GET.get('name')
    return JsonResponse({"message": "I'm trying to free your mind, {}. But I can only show you the door. You're the one that has to walk through it.".format(name)})

