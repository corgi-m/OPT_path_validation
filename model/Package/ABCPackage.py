from model.Package.ABCPackageHelper import ABCPackageHelper


class ABCPackage(ABCPackageHelper):
    index = 0

    def __init__(self):
        self.id = None
        self.PATH = None
        self.timestamp = None
        self.payload = None

    @classmethod
    def index_add(cls):
        cls.index += 1

    def get_id(self):
        return self.id

    def get_PATH(self):
        return self.PATH

    def get_payload(self):
        return self.payload
