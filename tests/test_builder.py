from contextlib import contextmanager
from filecmp import dircmp
from tempfile import mkdtemp
from shutil import rmtree
from unittest import TestCase


@contextmanager
def temp_folder():
    tmp_dir = mkdtemp()
    try:
        yield tmp_dir
    finally:
        rmtree(tmp_dir)

class DummyLogger(object):
    def info(self, *args, **kwargs): pass
    debug = warning = info


class BuilderFunctionalTest(object):

    def setUp(self):
        import os
        here = os.path.dirname(__file__)
        self.setUpTestDir(here)
        self.config_file = os.path.join(self.test_site_dir, 'sohoconf.py')
        self.expected_dir = os.path.join(self.test_site_dir, 'www')

    def setUpTestDir(self, here):
        import os
        self.test_site_dir = os.path.join(here, 'fixtures', self.test_site)

    def _make_builder(self, options, **custom_settings):
        from soho.builder import Builder
        from soho.cli import get_settings
        settings = get_settings(options)
        self.assertIn('logger', settings.keys())
        settings.update(custom_settings)
        settings['logger'] = DummyLogger()
        return Builder(**settings)

    def assertBuilderOutput(self, out_dir, expected_dir):
        diff = dircmp(out_dir, expected_dir)
        self.assertEqual(diff.left_only, [])
        self.assertEqual(diff.right_only, [])
        self.assertEqual(diff.diff_files, [])

    def test_builder(self):
        from .base import make_options
        options = make_options(config_file=self.config_file)
        with temp_folder() as out_dir:
            builder = self._make_builder(options=options, out_dir=out_dir)
            builder.build()
            self.assertBuilderOutput(out_dir, self.expected_dir)


class TestSite1(BuilderFunctionalTest, TestCase):

    test_site = 'site1'

    # inherits 'test_builder()' from BuilderFunctionalTest

    def test_builder_dry_run(self):
        import os
        from .base import make_options
        options = make_options(config_file=self.config_file, do_nothing=True)
        with temp_folder() as out_dir:
            builder = self._make_builder(options=options, out_dir=out_dir)
            builder.build()
            self.assertEqual(os.listdir(out_dir), [])

    def test_builder_build_twice(self):
        from .base import make_options
        options = make_options(config_file=self.config_file)
        with temp_folder() as out_dir:
            builder = self._make_builder(options=options, out_dir=out_dir)
            builder.build()
            # build again
            builder = self._make_builder(options=options, out_dir=out_dir)
            builder.build()
            self.assertBuilderOutput(out_dir, self.expected_dir)


class TestSite2(BuilderFunctionalTest, TestCase):
    test_site = 'site2'
    # inherits 'test_builder()' from BuilderFunctionalTest


class TutorialFunctionalTest(BuilderFunctionalTest):
    # Our base class to test all parts of the tutorials.
    def setUpTestDir(self, here):
        import os
        self.test_site_dir = os.path.join(
            here, '..', 'docs', '_tutorial', self.test_site)


class TestTutorialIntro(TutorialFunctionalTest, TestCase):
    test_site = '1-intro'


class TestTutorialAssets(TutorialFunctionalTest, TestCase):
    test_site = '2-assets'


class TestTutorialMetadata(TutorialFunctionalTest, TestCase):
    test_site = '3-metadata'


class TestTutorialI18n(TutorialFunctionalTest, TestCase):
    test_site = '4-i18n'
