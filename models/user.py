from models import Model
from .todo import Todo
from utils import sha256


class User(Model):
    ROLE_ADMIN = 1
    ROLE_USER = 10

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.note = form.get('note', '')
        self.id = form.get('id', None)
        # admin or user
        # 1 for admin
        # 10 for user
        self.role = int(form.get('role', self.ROLE_USER))

    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def validate_login(self):
        if self.find_by(username=self.username, password=self.encrypt_password(self.password)):
            return True
        return False

    @staticmethod
    def encrypt_password(password, salt='fj;dlsahf21'):
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    def validate_register(self):
        self.password = self.encrypt_password(self.password)
        if self.find_by(username=self.username) is None and len(self.password) > 5:
            self.save()
            return True
        return False

    def validate_update(self):
        self.password = self.encrypt_password(self.password)
        if self.find_by(username=self.username):
            self.save()
            return True
        return False

    def todo_list(self):
        items = []
        for item in Todo.all():
            if item.user_id == self.id:
                items.append(item)
        return items
