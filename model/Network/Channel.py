from tools.tools import strcat


class Channel:
    def __init__(self, index, source, destination, data=""):
        self.id = index
        self.source = source
        self.destination = destination
        self.data = data

    def __repr__(self):
        return strcat("Channel ", self.id, ': ', self.source.id, ' -> ', self.destination.id)

    def transfer(self, package):
        self.destination.receive(package)
        return
