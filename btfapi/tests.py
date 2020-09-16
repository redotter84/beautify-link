from django.test import TestCase
import json
import random
import requests
import string
from .random_generator import RandomGenerator
from .models import Link
from . import views

class AuxiliaryFunctionsTestCase(TestCase):
    def test_check_site(self):
        f = lambda x: views.check_site(x)
        self.assertTrue(f('https://google.com'))
        self.assertFalse(f('https://google.com/meow'))
        self.assertFalse(f('google.com'))
        self.assertFalse(f('http:google.com'))
        self.assertTrue(f('https://drive.google.com/'))
        self.assertTrue(f('http://кто.рф'))
        self.assertTrue(f('https://www.google.com/search?q=hello%26op=hello'))
    def test_check_code(self):
        f = lambda x: views.check_code(x);
        self.assertTrue(f('a-sdDvv7'))
        self.assertTrue(f('1'))
        self.assertFalse(f('hello_there'))
        self.assertTrue(f('hello-there'))
        self.assertFalse(f('hello.there'))
        self.assertFalse(f('кто-то'))
    def test_random_generator(self):
        for i in range(100):
            length = random.randint(1, 20)
            s = RandomGenerator.generate_string(length)
            self.assertTrue(views.check_code(s))
    def test_code_exists(self):
        f = lambda x: views.code_exists(x)
        link = Link.objects.create(code='test-code-exists-1', url='https://google.com')
        self.assertTrue(f('test-code-exists-1'))
        self.assertFalse(f('test-code-exists-2'))
    def test_generate_code(self):
        f = lambda x: views.generate_code(x)
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        digits = string.digits
        pool = lower + upper + digits
        for i in range(len(pool) - 1):
            link = Link.objects.create(code=f'{pool[i]}', url='https://google.com')
        code = f(1)
        self.assertFalse(views.code_exists(code))

class ReadCreateLinkTestCase(TestCase):
    def setUp(self):
        Link.objects.create(code='google', url='https://google.com')
    def create_link_query(self, url, code=None):
        href = f'/btfapi/create-link'
        r = self.client.post(href, { 'code': code, 'url': url }, content_type='application/json')
        return r
    def read_link_query(self, code):
        href = f'/btfapi/read-link'
        r = self.client.post(href, { 'code': code }, content_type='application/json')
        return r
    def test_read_link(self):
        # good
        r = self.read_link_query(code='google')
        payload = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(payload['data']['code'], 'google')
        self.assertEqual(payload['data']['url'], 'https://google.com')
        # bad
        r = self.read_link_query(code='roogle')
        payload = json.loads(r.content)
        self.assertEqual(r.status_code, 404)
    def test_create_link(self):
        # good
        r = self.create_link_query(url='https://google.com', code='google-test')
        payload = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(payload['data']['code'], 'google-test')
        self.assertEqual(payload['data']['url'], 'https://google.com')
        # bad url
        r = self.create_link_query(url='https://google.com/meow', code='meow')
        payload = json.loads(r.content)
        self.assertEqual(r.status_code, 400)
        # bad code
        r = self.create_link_query(url='https://google.com', code='google_test')
        payload = json.loads(r.content)
        self.assertEqual(r.status_code, 400)
        # code already exists
        r = self.create_link_query(url='https://google.com', code='google')
        payload = json.loads(r.content)
        self.assertEqual(r.status_code, 400)
