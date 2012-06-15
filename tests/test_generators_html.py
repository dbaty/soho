from unittest import TestCase


class TestHTMLGenerator(TestCase):

    def _make_one(self):
        from soho.generators.html import HTMLGenerator
        return HTMLGenerator()

    def test_basics(self):
        import os.path
        generator = self._make_one()
        here = os.path.dirname(__file__)
        path = os.path.join(here, 'fixtures', 'test1.html')
        meta, html = generator.generate(path)
        self.assertEqual(meta, {})
        self.assertEqual(html, '<p>This is a test.</p>')

    def test_with_metadata_file(self):
        import os.path
        generator = self._make_one()
        here = os.path.dirname(__file__)
        path = os.path.join(here, 'fixtures', 'test2.html')
        meta, html = generator.generate(path)
        self.assertEqual(meta, {'foo': 'Value of foo'})
        self.assertEqual(html, '<p>This is another test.</p>')
