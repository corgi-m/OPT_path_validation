from tools.tools import strcat


class Channel:
    def __init__(self, id, source, destination, data=""):
        self.__id = id
        self.__source = source
        self.__destination = destination
        self.__data = data

    def __repr__(self):
        return strcat("Channel ", self.__id, ': ', self.__source.get_id(), ' -> ', self.__destination.get_id())

    def get_id(self):
        return self.__id

    def get_source(self):
        return self.__source

    def get_destination(self):
        return self.__destination

    def get_data(self):
        return self.__data

    def transfer(self, package):
        self.__destination.receive(package)
        return
