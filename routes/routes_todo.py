from models.todo import Todo
from .routes_user import require_login
from utils import log, render_template, http_response, redirect
from . import router

# 路由字典
# key 是路由(路由就是 path)
# value 是路由处理函数(就是响应)
# route_dict = {}


@router.route('/todo')
@require_login
def index(request):
    u = request.login_user
    todo_list = Todo.find_all(user_id=u.id)
    return http_response(render_template('todo_index.html', todo_list=todo_list))


@router.route('/todo/edit')
@require_login
def edit(request):
    u = request.login_user
    todo_id = int(request.query.get('id', -1))
    log('to_do_id***********', str(todo_id))
    t = Todo.find_by(id=todo_id)
    if t.user_id != u.id:
        return redirect('/login')
    return http_response(render_template('todo_edit.html', todo=t))


@router.route('/todo/add')
@require_login
def add(request):
    u = request.login_user
    if request.method == 'POST':
        # 'title=aaa'
        # {'title': 'aaa'}
        form = request.form
        form.user_id = u.id
        t = Todo.new(form)
        print('routes todo add: user is {}'.format(u.__dict__))
        t.save()
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/todo')


@router.route('/todo/update')
@require_login
def update(request):
    """
    用于增加新 todo 的路由函数
    """
    u = request.login_user
    if request.method == 'POST':
        form = request.form
        todo_id = int(request.query.get('id', -1))
        t = Todo.find_by(id=todo_id)
        if t and t.user_id == u.id:
            Todo.update(todo_id, form)
    return redirect('/todo')


@router.route('/todo/delete')
@require_login
def delete_todo(request):
    u = request.login_user
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    if t is None or t.user_id != u.id:
        return redirect('/login')
    t.remove()
    return redirect('/todo')
