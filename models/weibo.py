from models import Model


class Weibo(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id')

    def comments(self):
        return [c for c in Comment.all() if c.tweet_id == self.id]


# 评论类
class Comment(Model):
    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', user_id)
        self.weibo_id = form.get('tweet_id', -1)
