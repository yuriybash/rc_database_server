import abc


class BaseStorage():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def store(self):
        pass

    @abc.abstractmethod
    def retrieve(self):
        pass

class InMemoryStorage():

    CONTAINER = {}

    def store(self, key, val):
        self.CONTAINER[key] = val

    def retrieve(self, key):
        return self.CONTAINER.get(key)
