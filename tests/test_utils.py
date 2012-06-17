from collections import namedtuple
import time
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

    def test_no_keys(self):
        registry = {}
        self.assertRaises(ValueError,
                          self._call_fut,
                          registry, 'soho.renderers.zpt.ZPTRenderer')

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


class TestReadFileMetadata(TestCase):
    def _call_fut(self, path):
        from soho.utils import read_file_metadata
        return read_file_metadata(path)

    def test_basics(self):
        import os
        here = os.path.dirname(__file__)
        path = os.path.join(here, 'fixtures', 'test2.html')
        self.assertEqual(self._call_fut(path), {'foo': 'Value of foo'})

    def test_file_does_not_exist(self):
        self.assertEqual(self._call_fut('/does/not/exist'), {})


class TestReadDirMetadata(TestCase):
    def _call_fut(self, path):
        from soho.utils import read_dir_metadata
        return read_dir_metadata(path)

    def test_basics(self):
        import os
        here = os.path.dirname(__file__)
        path = os.path.join(here, 'fixtures')
        self.assertEqual(self._call_fut(path), {'foo': 'Value of foo'})

    def test_file_does_not_exist(self):
        self.assertEqual(self._call_fut('/does/not/exist'), {})


class TestHideIndexHtmlFrom(TestCase):

    def test_basics(self):
        from soho.utils import hide_index_html_from
        self.assertEqual(hide_index_html_from('foo'), 'foo')
        self.assertEqual(hide_index_html_from('index.html'), '')
        self.assertEqual(hide_index_html_from('/index.html'), '')
        self.assertEqual(hide_index_html_from('foo/index.html'), 'foo')


def mock_os_stat(path):
    t = {'foo': 1234567890,
         'bar': 123456789}[path]
    return namedtuple('Stat', 'st_mtime')(t)


class TestSitemap(TestCase):

    def _make_one(self):
        from soho.utils import Sitemap
        return Sitemap()

    # Your 'time.localtime(t)' may return a different date than mine
    # if we are not on the same timezone. Here we use 'time.gmtime()'
    # instead which will return the same result everywhere.
    @mock.patch('time.localtime', time.gmtime)
    @mock.patch('os.stat', mock_os_stat)
    def test_basics(self):
        try:  # pragma: no coverage
            from StringIO import StringIO
        except:  # pragma: no coverage
            # Python 3
            from io import StringIO  # pyflakes: ignore
        b = 'http://exemple.com/'
        sitemap = self._make_one()
        sitemap.add('foo', b + 'foo', 'monthly', 0.5)
        sitemap.add('bar', b + 'bar', 'weekly', '0.4')
        out = StringIO()
        sitemap.write(out)
        expected = [
            '<?xml version="1.0" encoding="utf-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            '  <url>',
            '    <loc>http://exemple.com/bar</loc>',
            '    <lastmod>1973-11-29</lastmod>',
            '    <changefreq>weekly</changefreq>',
            '    <priority>0.4</priority>',
            '  </url>',
            '',
            '  <url>',
            '    <loc>http://exemple.com/foo</loc>',
            '    <lastmod>2009-02-13</lastmod>',
            '    <changefreq>monthly</changefreq>',
            '    <priority>0.5</priority>',
            '  </url>',
            '</urlset>']
        self.assertEqual(out.getvalue().split('\n'), expected)
