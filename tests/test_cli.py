from unittest import TestCase


class TestGetSettings(TestCase):

    def _call_fut(self, options):
        from soho.cli import get_settings
        return get_settings(options)

    def test_basics(self):
        from logging import Logger
        import os
        import re
        from .base import make_options
        here = os.path.dirname(__file__)
        config_dir = os.path.join(here, 'fixtures', 'site1')
        config_file = os.path.join(config_dir, 'sohoconf.py')
        options = make_options(config_file=config_file)
        settings = self._call_fut(options)
        ignore_files = ('.*\.DS_Store$', '.*~$', '.*ignored.txt$')
        ignore_files = [re.compile(exp) for exp in ignore_files]
        path = lambda p: os.path.join(config_dir, p)
        logger = settings.pop('logger')
        self.assertIsInstance(logger, Logger)
        self.assertEqual(settings,
                         {'asset_dir': path('assets'),
                          'assets_only': False,
                          'base_url': 'http://exemple.com',
                          'do_nothing': False,
                          'force': False,
                          'hide_index_html': True,
                          'ignore_files': ignore_files,
                          'locale_dir': path('locale'),
                          'out_dir': path('www'),
                          'sitemap': 'sitemap.xml',
                          'src_dir': path('src'),
                          'template': 'layout.pt',
                          'template_dir': path('templates'),
                          })
