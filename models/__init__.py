import json

from utils import log


def save(data, path):
    """
    Saving data in specific path
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, mode='w', encoding='utf-8') as f:
        log('saving', path, s, data)
        f.write(s)


def load(path):
    """
    Load data from specific path
    """
    with open(path, encoding='utf-8') as f:
        s = f.read()
        log('loading', s)
        return json.loads(s)


class Model:
    @classmethod
    def db_path(cls):
        class_name = cls.__name__
        path = 'db/{}.txt'.format(class_name)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        """
        find an object by specified attr
        """
        ms = cls.all()
        keys = kwargs.keys()
        log('ms', ms)
        log('keys', kwargs)
        for m in ms:
            d = m.__dict__
            try:
                if all(d[k] == kwargs[k] for k in keys):
                    return m
            except KeyError as e:
                log('Method {}.find_by called but raise an error: '.format(cls.__name__), e)
                return None
        return None

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def find_all(cls, **kwargs):
        """
        find all objects by specified attr
        """
        wanted = []
        ms = cls.all()
        keys = kwargs.keys()
        for m in ms:
            d = m.__dict__
            try:
                if all(d[k] == kwargs[k] for k in keys):
                    wanted.append(m)
            except KeyError as e:
                log('Method {}.find_by called but raise an error: '.format(cls.__name__), e)
                return []
        return wanted

    def save(self):
        ms = self.all()
        if (not hasattr(self, 'id')) or self.id is None:
            if len(ms) > 0:
                self.id = ms[-1].id + 1
            else:
                self.id = 0
            ms.append(self)
        else:
            # search
            index = -1
            for i, m in enumerate(ms):
                if m.id == self.id:
                    index = i
                    break
            if index > -1:
                ms[index] = self

        log('models', ms)
        log('self.id', self.id)

        data = [m.__dict__ for m in ms]
        path = self.db_path()
        save(data, path)

    def remove(self):
        ms = self.all()
        if self.id is not None:
            # search
            index = -1
            for i, m in enumerate(ms):
                if m.id == self.id:
                    index = i
                    break
            if index > -1:
                del ms[index]
                data = [m.__dict__ for m in ms]
                path = self.db_path()
                save(data, path)

    def __repr__(self):
        class_name = self.__class__.__name__
        data = '\n'.join('{}: {}'.format(k, v) for k, v in self.__dict__.items())
        return '< {}\n{} >\n'.format(class_name, data)
