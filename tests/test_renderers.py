from unittest import TestCase

import mock


class DummyRenderer(object):
    def __init__(self, *args, **kwargs):
        self.log = [args, kwargs]


class TestGetGenerator(TestCase):

    def _call_fut(self, path, *args, **kwargs):
        from soho.renderers import get_renderer
        return get_renderer(path, *args, **kwargs)

    def test_unknown_ext(self):
        self.assertEqual(self._call_fut('unknown'), None)

    @mock.patch('soho.renderers.registry',
                new_callable=lambda: {'ext': DummyRenderer})
    def test_known_ext(self, mock_registry):
        got = self._call_fut('file.ext', 'foo', bar='bar')
        expected = [('file.ext', 'foo', ), {'bar': 'bar'}]
        self.assertIsInstance(got, DummyRenderer)
        self.assertEqual(got.log, expected)
