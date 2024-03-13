from abc import ABC


class ABCPackage(ABC):
    layer = 'ABCLayer'

    def __init__(self):
        self.id = None

    def __repr__(self):
        class_name = self.__class__.__name__
        attributes = ', '.join(f'{key}={value}' for key, value in self.__dict__.items())
        return f'{class_name}({attributes})'

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    @classmethod
    def get_layer(cls):
        return cls.layer

    def get_id(self):
        return self.id
