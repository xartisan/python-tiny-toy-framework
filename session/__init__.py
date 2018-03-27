from collections import UserDict
from models.user import User


# 内存中的session
class Session(UserDict):
    def get_user(self, request):
        session_id = request.cookies.get('user', '')
        user_id = self.get(session_id)
        if user_id is None:
            return None
        return User.find(user_id)


session = Session()
