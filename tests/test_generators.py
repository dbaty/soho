from unittest import TestCase

import mock


def dummy_generator(*args, **kwargs):
    return (args, kwargs)


class TestGetGenerator(TestCase):

    def _call_fut(self, path, *args, **kwargs):
        from soho.generators import get_generator
        return get_generator(path, *args, **kwargs)

    def test_unknown_ext(self):
        self.assertEqual(self._call_fut('unknown'), None)

    @mock.patch('soho.generators.registry',
                new_callable=lambda: {'ext': dummy_generator})
    def test_known_ext(self, mock_registry):
        expected = (('foo', ), {'bar': 'bar'})
        self.assertEqual(self._call_fut('file.ext', 'foo', bar='bar'), expected)
