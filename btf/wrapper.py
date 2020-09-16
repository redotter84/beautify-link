import requests

class ApiResponse:
    def __init__(self, status, json):
        self.status = status
        self.json = json

class Wrapper:
    @staticmethod
    def read_link(code, site):
        href = f'{site}btfapi/read-link'
        r = requests.post(href, json={ 'code': code })
        return ApiResponse(r.status_code, r.json())

    @staticmethod
    def create_link(url, code=None, site=None):
        href = f'{site}btfapi/create-link'
        r = requests.post(href, json={ 'code': code, 'url': url })
        return ApiResponse(r.status_code, r.json())
