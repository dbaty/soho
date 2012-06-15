from unittest import TestCase


class TestInterpolate(TestCase):

    def _call_fut(self, s, mapping):
        from soho.i18n import interpolate
        return interpolate(s, mapping)

    def test_basics(self):
        self.assertEqual(self._call_fut('foo', {'foo': 'Value of foo'}), 'foo')
        self.assertEqual(self._call_fut('${foo} bar', {'foo': 'Value of foo'}),
                         'Value of foo bar')
        self.assertEqual(self._call_fut('${foo} ${foo}',
                                        {'foo': 'Value of foo'}),
                         'Value of foo Value of foo')
        self.assertEqual(self._call_fut('${foo} ${bar}',
                                        {'foo': 'Value of foo',
                                         'bar': 'Value of bar'}),
                         'Value of foo Value of bar')

    def test_unknown_var(self):
        self.assertEqual(self._call_fut('${foo}', {'bar': 'bar'}), '${foo}')

    def test_empty_values(self):
        self.assertEqual(self._call_fut('foo', {}), 'foo')
        self.assertEqual(self._call_fut('foo ${bar}', {}), 'foo ${bar}')


class TestTranslatorWrapper(TestCase):

    def _make_one(self, locale_dir):
        from soho.i18n import TranslatorWrapper
        return TranslatorWrapper(locale_dir)

    def test_basics(self):
        import os
        here = os.path.dirname(__file__)
        locale_dir = os.path.join(here, 'fixtures', 'site1', 'locale')
        wrapper = self._make_one(locale_dir)
        for locale, msgid, domain, mapping, expected in (
            ('fr', 'Web site', 'test', {}, 'Site web'),
            ('fr', 'My name is ${name}.', 'test', {'name': 'John'},
             'Mon nom est John.'),
            # Unknown locale
            ('pt', 'Web site', 'test', {}, 'Web site'),
            # Unknown msgid
            ('fr', 'Unknown msgid', 'test', {}, 'Unknown msgid'),
            # Unknown domain
            ('fr', 'Web site', 'unknown', {}, 'Web site')):
            translated = wrapper.translate(locale, msgid, domain, mapping)
            self.assertEqual(translated, expected)
