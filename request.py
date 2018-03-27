import urllib.parse
from utils import log
import json


class Request:
    def __init__(self):
        self.remote_addr = None
        self.method = 'GET'
        self.path = '/'
        self.query = None
        self.protocol = 'HTTP/1.1'
        self.headers = None
        self.cookies = None
        self.body = None

    @staticmethod
    def from_http_and_address(http_text, address):
        req = http_text.split('\r\n\r\n', 1)
        log('req', req)
        head = req[0]
        body = req[1] if len(req) == 2 else ''
        request_line, *request_headers = head.split('\r\n')
        request_line_parts = request_line.split(' ', 2)
        # in case of '/'
        path_with_query = request_line_parts[1].rstrip('/') or '/'
        path, query = Request.parse_path(path_with_query)
        # compose new request object
        request = Request()
        request.remote_addr = address
        request.method = request_line_parts[0]
        request.path = path
        request.query = query
        request.protocol = request_line_parts[-1]
        request.set_headers(request_headers)
        request.body = body
        return request

    def parse_cookies(self):
        self.cookies = {}
        c = self.headers.get('Cookie', '')
        for item in c.split('; '):
            if '=' in item:
                k, v = item.split('=')
                self.cookies[k] = v

    def set_headers(self, fields):
        self.headers = {}
        for field in fields:
            k, v = field.split(': ', 1)
            self.headers[k] = v
        self.parse_cookies()

    @property
    def form(self):
        """
        Parse the body of the request and returns a form
        :return: a dict parsed from the body of the request
        """
        if not hasattr(self, '_request_form'):
            form = {}
            if self.body:
                kvs = self.body.split('&')
                for kv in kvs:
                    k, v = kv.split('=')
                    k, v = urllib.parse.unquote_plus(k), urllib.parse.unquote_plus(v)
                    form[k] = v
            setattr(self, '_request_form', form)
        return getattr(self, '_request_form')

    @property
    def json(self):
        return json.loads(self.body)

    @staticmethod
    def parse_path(path: str):
        query = {}
        if '?' in path:
            path, query_string = path.split('?', 1)
            for item in query_string.split('&'):
                k, v = item.split('=')
                query[k] = v
        log('path and query is', path, query)
        return path, query

    def __repr__(self):
        return self.__class__.__name__ + repr(self.__dict__)
