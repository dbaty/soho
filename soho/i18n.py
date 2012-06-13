from gettext import GNUTranslations
import os

from translationstring import Translator


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
            return msgid
        return translator(msgid, domain, mapping)
