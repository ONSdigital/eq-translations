import unittest

from app.utils import get_parent_pointer, find_pointers_containing, find_pointers_to


class TestPointers(unittest.TestCase):

    def test_find_pointers_containing_root(self):
        schema = {
            'test': ''
        }

        pointers = [p for p in find_pointers_containing(schema, 'test')]

        assert pointers == []

    def test_find_pointers_containing_element(self):
        schema = {
            'this': 'is',
            'a': {
                'test': 'schema'
            }
        }

        pointers = find_pointers_containing(schema, 'test')

        assert '/a' in pointers

    def test_find_pointers_containing_list(self):
        schema = {
            'this': 'is',
            'a': {
                'test': [{
                    'item': {}
                }, {
                    'item': {}
                }, {
                    'item': {}
                }, {
                    'item': {}
                }, {
                    'item': {}
                }]
            }
        }

        pointers = find_pointers_containing(schema, 'item')

        assert '/a/test/0' in pointers
        assert '/a/test/1' in pointers
        assert '/a/test/2' in pointers
        assert '/a/test/3' in pointers
        assert '/a/test/4' in pointers

    def test_find_pointers_to_root(self):
        schema = {
            'test': {},
            'foo': {},
            'bar': {}
        }

        pointers = find_pointers_to(schema, 'test')

        assert '/test' in pointers

    def test_find_pointers_to_element(self):
        schema = {
            'this': 'is',
            'a': {
                'test': 'schema'
            }
        }

        pointers = find_pointers_to(schema, 'test')

        assert '/a/test' in pointers

    def test_find_pointers_to_list(self):
        schema = {
            'this': 'is',
            'a': {
                'test': [{
                    'item': {}
                }, {
                    'item': {}
                }, {
                    'item': {}
                }, {
                    'item': {}
                }, {
                    'item': {}
                }]
            }
        }

        pointers = find_pointers_to(schema, 'item')

        assert '/a/test/0/item' in pointers
        assert '/a/test/1/item' in pointers
        assert '/a/test/2/item' in pointers
        assert '/a/test/3/item' in pointers
        assert '/a/test/4/item' in pointers

    def test_get_parent_pointer(self):
        option_parent_pointer = get_parent_pointer('/questions/0/answers/0/options/0/label')
        answer_parent_pointer = get_parent_pointer('/questions/0/answers/0/label')

        assert option_parent_pointer == '/questions/0/answers/0/options/0'
        assert answer_parent_pointer == '/questions/0/answers/0'
