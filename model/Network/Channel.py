from tools.tools import strcat


class Channel:
    def __init__(self, id, source, destination, data=""):
        self.id = id
        self.source = source
        self.destination = destination
        self.data = data

    def __repr__(self):
        return strcat("Channel ", self.id, ': ', self.source.id, ' -> ', self.destination.id)

    def get_id(self):
        return self.id

    def transfer(self, package):
        self.destination.receive(package)
        return
