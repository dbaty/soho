from gettext import GNUTranslations
import os
import re

from translationstring import Translator


INTERPOLATE_REGEXP = re.compile('\${(\w*)}')


def interpolate(s, mapping):
    """Interpolate params in the given string ``s`` with values
    provided in ``mapping`` (if any).
    """
    if not mapping:
        return s
    def _sub(matchobj):
        var = matchobj.group(1)
        return mapping.get(var, matchobj.group(0))
    return INTERPOLATE_REGEXP.sub(_sub, s)


class TranslatorWrapper(object):
    """A wrapper that hold instances of ``gettext.GNUTranslations``
    and take care of choosing the right one depending on the domain
    and the locale that are requested at translation time.
    """

    def __init__(self, locale_dir):
        self.translators = {}
        self.load_translations(locale_dir)

    def load_translations(self, locale_dir):
        """Load translations from files located in ``locale_dir``."""
        for locale in os.listdir(locale_dir):
            locale_path = os.path.join(locale_dir, locale)
            if not os.path.isdir(locale_path):
                continue
            self.translators[locale] = {}
            msg_dir_path = os.path.join(locale_path, 'LC_MESSAGES')
            for filename in os.listdir(msg_dir_path):
                if not filename.endswith('.mo'):
                    continue
                domain = filename[:-3]
                mo_path = os.path.join(msg_dir_path, filename)
                with open(mo_path, 'rb') as fp:
                    translator = Translator(GNUTranslations(fp))
                    self.translators[locale][domain] = translator

    def translate(self, locale, msgid, domain, mapping):
        """Translate ``msgid`` in the requested ``locale``."""
        try:
            translator = self.translators[locale][domain]
        except KeyError:
            return interpolate(msgid, mapping)
        return translator(msgid, domain, mapping)
