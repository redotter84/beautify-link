from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import json
import requests
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from urllib.parse import urlparse
from . import response
from .serializers import LinkSerializer
from .models import Link
from .random_generator import RandomGenerator

CODE_LENGTH = 6

class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

def code_exists(code):
    links = Link.objects.filter(code=code)
    return links.exists()

def generate_code(length):
    code = RandomGenerator.generate_string(length)
    while code_exists(code):
        code = RandomGenerator.generate_string(length)
    return code

def check_site(url):
    parse = urlparse(url)
    if not parse.scheme or not parse.netloc:
        return False
    r = requests.get(url)
    return r.status_code == 200

def check_code(code):
    for c in code:
        upper = ord('A') <= ord(c) <= ord('Z')
        lower = ord('a') <= ord(c) <= ord('z')
        digit = ord('0') <= ord(c) <= ord('9')
        hyphen = c == '-'
        if not (upper or lower or digit or hyphen):
            return False
    return True

@api_view(['GET'])
def read_link(request):
    payload = json.loads(request.body)
    try:
        code = payload['code']
        link = Link.objects.get(code=code)
        serializer = LinkSerializer(link)
        return response.ok(serializer.data)
    except ObjectDoesNotExist as err:
        return response.code_not_found(payload['code'])
    except Exception:
        return response.something_wrong()

@api_view(['POST'])
def create_link(request):
    payload = json.loads(request.body)
    try:
        code = payload['code']
        if code == None:
            code = generate_code(CODE_LENGTH)
        url = payload['url']
        if not check_code(code):
            return response.incorrect_code(code)
        if code_exists(code):
            return response.code_exists(code)
        if not check_site(url):
            return response.incorrect_url(url)
        link = Link.objects.create(code=code, url=url)
        serializer = LinkSerializer(link)
        return response.ok(serializer.data)
    except Exception:
        return response.something_wrong()
