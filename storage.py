import abc


class BaseStorage():
    """
    Interface for all supported storage engines.
    """
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
    """
    In-memory storage engine. Uses a dict internally.
    """

    CONTAINER = {}

    def store(self, key, val):
        """
        Store a given key-value pair.

        :param key: the key
        :type key: any hashable type (has `__hash__` method)
        :param val: the value
        :type val: any
        :return: None
        :rtype: None
        """
        self.CONTAINER[key] = val

    def store_multiple(self, keys_vals):
        """
        Store multiple key-value pairs

        :param keys_vals: keys, values (e.g. {'fruit': 'plum', 'color': 'red')
        :type keys_vals: dict
        :return: None
        :rtype: None
        """

        for k, v in keys_vals.iteritems():
            self.store(k, v)

    def retrieve(self, key):
        """
        Retrieve a value for a given key.

        :param key: the key
        :type: any hashable type
        :return: the value
        :rtype: any
        """
        return self.CONTAINER.get(key)
