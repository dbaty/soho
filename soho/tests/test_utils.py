from unittest import TestCase

import mock


class TestRegisterPlugin(TestCase):

    def _call_fut(self, registry, spec, *keys):
        from soho.utils import register_plugin
        return register_plugin(registry, spec, *keys)

    def test_basics(self):
        from soho.renderers.zpt import ZPTRenderer
        registry = {}
        self._call_fut(registry, 'soho.renderers.zpt.ZPTRenderer', 'zpt')
        self.assertEqual(registry, {'zpt': ZPTRenderer})

    def test_multiple_keys(self):
        from soho.renderers.zpt import ZPTRenderer
        registry = {}
        self._call_fut(registry, 'soho.renderers.zpt.ZPTRenderer', 'zpt', 'pt')
        self.assertEqual(registry, {'zpt': ZPTRenderer,
                                    'pt': ZPTRenderer})

    @mock.patch('logging.debug')
    def test_import_error_is_logged(self, mock_debug):
        registry = {}
        self._call_fut(registry, 'does.not.exist', 'foo')
        self.assertEqual(registry, {})
        error = 'Could not import plugin: "%s".'
        mock_debug.assert_called_with(error, 'does.not.exist')


class TestHideIndexHtmlFrom(TestCase):

    def test_basics(self):
        from soho.utils import hide_index_html_from
        self.assertEqual(hide_index_html_from('foo'), 'foo')
        self.assertEqual(hide_index_html_from('index.html'), '')
        self.assertEqual(hide_index_html_from('/index.html'), '')
        self.assertEqual(hide_index_html_from('foo/index.html'), 'foo')
