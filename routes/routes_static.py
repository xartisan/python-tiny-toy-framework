from routes import router


@router.route('/static')
def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    <img src="/static?file=doge.gif"/>
    GET /static?file=doge.gif
    path, query = response_for_path('/static?file=doge.gif')
    path  '/static'
    query = {
        'file', 'doge.gif',
    }
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n' + f.read()
        return img
