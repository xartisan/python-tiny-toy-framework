import random
import re
import os
import time

from jinja2 import FileSystemLoader, Environment
import hashlib

REPLACE_PATTERN = re.compile(r'{{\s*([a-zA-Z\d_]+)\s*}}')


def log(*args, **kwargs):
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def random_string(n: int) -> str:
    to_choose = 'abcdefghijklmnopqrstuvwxyz1234567890'
    s = []
    for i in range(n):
        s.append(to_choose[random.randint(0, len(to_choose) - 1)])
    return ''.join(s)


def render_html(html, **kwargs):
    def handle_match(m):
        match_word = m.group(1)
        return kwargs.get(match_word, '{{ ' + match_word + ' }}')

    return REPLACE_PATTERN.sub(handle_match, html)


def response_with_headers(headers, code=200, message='OK'):
    """
    Content-Type: text/html
    Set-Cookie: user=gua
    """
    header = 'HTTP/1.1 {} {}\r\n'.format(code, message)
    header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    return header


# __file__ 就是本文件的名字
# 得到用于加载模板的目录
path = '{}/templates/'.format(os.path.dirname(__file__))
# 创建一个加载器, jinja2 会从这个目录中加载模板
loader = FileSystemLoader(path)
# 用加载器创建一个环境, 有了它才能读取模板文件
env = Environment(loader=loader)


def render_template(path, **kwargs):
    t = env.get_template(path)
    return t.render(**kwargs)


def redirect(location, headers=None):
    h = {
        'Content-Type': 'text/html',
    }
    if headers is not None:
        h.update(headers)
    h['Location'] = location
    # 302 状态码的含义, Location 的作用
    header = response_with_headers(h, 302, "Redirect")
    r = header + '\r\n' + ''
    return r.encode(encoding='utf-8')


def http_response(body, headers=None):
    """
    headers 是可选的字典格式的 HTTP 头
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    if headers is not None:
        header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def sha256(ascii_str):
    return hashlib.sha256(ascii_str.encode('utf-8')).hexdigest()
