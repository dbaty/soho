from unittest import TestCase


class TestZPTRenderer(TestCase):

    def _make_one(self, filename, translate):
        from soho.renderers.zpt import ZPTRenderer
        return ZPTRenderer(filename, translate)

    def test_basics(self):
        import os
        here = os.path.dirname(__file__)
        filename = os.path.join(here, 'fixtures', 'test.pt')
        translate = lambda msgid, **kwargs: ''.join(reversed(msgid))
        renderer = self._make_one(filename, translate=translate)
        rendered = renderer.render(foo='Dynamic value.')
        self.assertEqual(rendered.strip(),
                         '\n'.join(('<p>This is a paragraph.</p>',
                                    '<p>Dynamic value.</p>',
                                    '<p>I am translated.</p>')))
