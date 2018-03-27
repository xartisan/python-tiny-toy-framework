from utils import log
from models.user import User
from utils import random_string, render_template, redirect, http_response
from routes import router
from session import session
from auth import require_login, require_admin


@router.route('/')
def index(request):
    """
    index controller
    """
    user = session.get_user(request)
    username = user.username if user else '游客'

    body = render_template('index.html', username=username)
    return http_response(body)


@router.route('/login')
def login(request):
    """
    login controller
    """
    if request.method == 'POST':
        form = request.form
        u = User.new(form)
        if u.validate_login():
            user = User.find_by(username=u.username)
            session_id = random_string(20)
            session[session_id] = user.id
            headers = {'Set-Cookie': 'user={}'.format(session_id)}
            return redirect('/', headers)

    return http_response(render_template('login.html'))


@router.route('/register')
def register(request):
    if request.method == 'POST':
        form = request.form
        u = User.new(form)
        log(u.__dict__)
        if u.validate_register():
            return redirect('/login')
        else:
            return redirect('/register')

    body = render_template('register.html')
    return http_response(body)


# message_list = []
#
#
# @route('/messages')
# def message(request):
#     log('本次请求的 method', request.method)
#     if request.method == 'POST':
#         form = request.form()
#         msg = Message.new(form)
#         log('post', form)
#         message_list.append(msg)
#         # 应该在这里保存 message_list
#     header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
#     body = template('html_basic.html')
#     # '#'.join(['a', 'b', 'c']) 的结果是 'a#b#c'
#     msgs = '<br>'.join([str(m) for m in message_list])
#     body = body.replace('{{messages}}', msgs)
#     r = header + '\r\n' + body
#     return r.encode(encoding='utf-8')


@router.route('/profile')
@require_login
def profile(request):
    user = request.login_user
    context = dict(
        username=user.username,
        password=user.password,
        note=user.note,
    )
    body = render_template('profile.html', **context)
    return http_response(body)


@router.route('/admin/users')
@require_admin
def view_users(request):
    u = User.find_all()
    body = render_template('admin/users.html', users=u)
    return http_response(body)


@router.route('/admin/user/update')
@require_admin
def update_user(request):
    request_form = request.form
    user_id = int(request_form.get('id', -1))
    new_password = request_form.get('password', '')
    user = User.find_by(id=user_id)
    if user:
        user.password = new_password
        if user.validate_update():
            user.save()
    return redirect('/admin/users')
