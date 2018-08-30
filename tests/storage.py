from __future__ import absolute_import
import unittest

from ..storage import BaseStorage, InMemoryStorage

class BaseStorageTest(unittest.TestCase):

    def test_sbcls_enforcement(self):

        class InvalidClass(BaseStorage):
            pass

        with self.assertRaises(TypeError):
            InvalidClass()

class InMemoryStorageTest(unittest.TestCase):

    def setUp(self):
        self.storage = InMemoryStorage()

    def test_store(self):
        self.storage.store('a', 'b')

        # pop to ensure container is empty at the end
        self.assertEqual(self.storage.CONTAINER.pop('a'), 'b')
        self.assertEqual(self.storage.CONTAINER, {})

    def test_store_multiple(self):
        self.storage.store_multiple({'c': 'd', 'e': 'f'})
        self.assertEqual(self.storage.CONTAINER.pop('c'), 'd')
        self.assertEqual(self.storage.CONTAINER.pop('e'), 'f')
        self.assertEqual(self.storage.CONTAINER, {})

    def test_retrieve(self):
        self.storage.store('a', 'b')
        self.assertEqual('b', self.storage.retrieve('a'))

if __name__ == '__main__':
    unittest.main()
