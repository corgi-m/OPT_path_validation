import random


class ABCPackageHelper:
    def __repr__(self):
        class_name = self.__class__.__name__
        attributes = ', '.join(f'{key}={value}' for key, value in self.__dict__.items())
        return f'{class_name}({attributes})'

    @staticmethod
    def gen_payload(size=None):
        size = random.randint(1, 65535) if size is None else size
        payload = random.randbytes(size)
        return payload

