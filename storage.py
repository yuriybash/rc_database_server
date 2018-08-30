import abc


class BaseStorage():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def store(self):
        pass

    @abc.abstractmethod
    def store_multiple(self):
        pass

    @abc.abstractmethod
    def retrieve(self):
        pass


class InMemoryStorage():

    CONTAINER = {}

    def store(self, key, val):
        self.CONTAINER[key] = val

    def store_multiple(self, keys_vals):
        for k, v in keys_vals.iteritems():
            self.store(k, v[0])

    def retrieve(self, key):
        return self.CONTAINER.get(key)
