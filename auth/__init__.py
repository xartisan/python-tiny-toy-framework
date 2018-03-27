from session import session
from utils import redirect, log
from models.user import User


def require_login(handler):
    def new_handler(request):
        user = session.get_user(request)
        if user is None:
            return redirect('/login')
        request.login_user = user
        log('login user is', user)
        return handler(request)

    return new_handler


def require_admin(handler):
    @require_login
    def new_handler(request):
        if request.login_user.role != User.ROLE_ADMIN:
            return redirect('/login')
        return handler(request)

    return new_handler
