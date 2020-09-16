from django.http import HttpResponse, HttpResponseRedirect
from .wrapper import Wrapper

def read_link(request, code):
    site = request.build_absolute_uri('/')
    link = Wrapper.read_link(code=code, site=site)
    if link.status != 200:
        return HttpResponse(link.json['error'])
    url = link.json['data']['url']
    return HttpResponseRedirect(url)

def create_link(request):
    if 'url' not in request.GET:
        return HttpResponse('There is nothing to create')
    url = request.GET['url']
    code = None
    if 'code' in request.GET:
        code = request.GET['code']
    site = request.build_absolute_uri('/')
    link = Wrapper.create_link(url=url, code=code, site=site)
    if link.status != 200:
        return HttpResponse(link.json['error'])
    code = link.json['data']['code']
    url_code = site + code
    return HttpResponse(f'Your code is <a href={url_code}>{url_code}</a>')
