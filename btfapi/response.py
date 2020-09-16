from django.http import JsonResponse
from rest_framework import status

def ok(data):
    return JsonResponse({ 'data': data }, safe=False, status=status.HTTP_200_OK)

def incorrect_code(code):
    return JsonResponse({ 'error': f'Bad code: {code}' }, safe=False, status=status.HTTP_400_BAD_REQUEST)

def incorrect_url(url):
    return JsonResponse({ 'error': f'Incorrect url: <a href={url}>{url}</a>' }, safe=False, status=status.HTTP_400_BAD_REQUEST)

def code_exists(code):
    return JsonResponse({ 'error': f'Code {code} already exists' }, safe=False, status=status.HTTP_400_BAD_REQUEST)

def something_wrong():
    return JsonResponse({ 'error': 'Something went wrong' }, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def code_not_found(code):
    return JsonResponse({ 'error': f'Code {code} is not found' }, safe=False, status=status.HTTP_404_NOT_FOUND)
