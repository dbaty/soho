from unittest import TestCase


class TestRSTGenerator(TestCase):

    def _make_one(self):
        from soho.generators.rst import RSTGenerator
        return RSTGenerator()

    def _call_generate(self, filename):
        import os.path
        generator = self._make_one()
        here = os.path.dirname(__file__)
        path = os.path.join(here, 'fixtures', filename)
        return generator.generate(path)

    def test_basics(self):
        meta, html = self._call_generate('test1.rst')
        self.assertEqual(meta, {})
        self.assertEqual(html, '<p>This is a <strong>test</strong>.</p>')

    def test_with_metadata_in_rst_file(self):
        meta, html = self._call_generate('test2.rst')
        self.assertEqual(meta, {'foo': 'Value of foo'})
        self.assertEqual(html, '<p>This is another <strong>test</strong>.</p>')

    def test_with_metadata_in_file(self):
        meta, html = self._call_generate('test3.rst')
        self.assertEqual(meta, {'foo': 'Inherited value of foo',
                                'bar': 'Overriden value of bar'})
        self.assertEqual(html, '<p>This is another <strong>test</strong>.</p>')

    def test_sphinx_directives(self):
        meta, html = self._call_generate('test-code-block.rst')
        expected = (
            '<div class="highlight-python">'
            '<table class="highlighttable"><tr>'
            '<td class="linenos">'
            '<div class="linenodiv"><pre>1</pre></div></td>'
            '<td class="code">'
            '<div class="highlight"><pre><span class="k">print</span> '
            '<span class="s">&#39;foo&#39;</span>\n</pre></div>\n</td>'
            '</tr>'
            '</table>'
            '</div>')
        self.assertEqual(html, expected)
