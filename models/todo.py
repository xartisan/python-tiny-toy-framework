import time
from models import Model


# 继承自 Model 的 Todo 类
class Todo(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.task = form.get('task', '')
        self.completed = False
        self.user_id = int(form.get('user_id'))

        self.created_time = form.get('created_time')
        self.updated_time = form.get('updated_time')
        if self.created_time is None:
            self.created_time = int(time.time())
            self.updated_time = self.created_time

    def ct(self, t=None, time_format='%m-%d %H:%M:%S'):
        """
        :return: created time
        """
        t = t or self.created_time
        local_time = time.localtime(t)
        return time.strftime(time_format, local_time)

    @classmethod
    def complete(cls, todo_id, completed=True):
        t = Todo.find(todo_id)
        if t:
            t.completed = completed
            t.save()
            return t

    def belongs_to(self, user_id):
        return self.user_id == user_id

    @classmethod
    def update(cls, todo_id, form):
        t = Todo.find(todo_id)
        if t is None:
            return
        attr_list = ['task', 'completed']
        for attr in attr_list:
            value = form.get(attr)
            if value:
                setattr(t, attr, value)
        t.updated_time = int(time.time())
        t.save()
