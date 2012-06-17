"""Define the ``ReSTGenerator``, which takes reStructuredText as input
and return HTML as output.
"""

import re

from docutils.writers.html4css1 import Writer as BaseWriter
from docutils.core import publish_parts

# Register Sphinx directives if Sphinx is available.
try:
    # Importing the 'code' module registers the directives.
    from sphinx.directives import code
    code  # makes pyflakes happy

    # 'sphinx.writers.html.HTMLTranslator' provides the necessary
    # visitors to handle extra directives defined by Sphinx. It needs
    # a builder. Some builders are defined in 'sphinx.builders.html'
    # but require attributes that we would have to mock (including
    # file paths). Therefore, we just mock the builder itself.
    from sphinx.highlighting import PygmentsBridge
    from sphinx.writers.html import HTMLTranslator
    class FakeBuilder(object):
        def __init__(self, *args, **kwargs):
            self.highlighter = PygmentsBridge()
            self.config = Mock('config')
    class Mock(object):
        def __init__(self, name):
            self.name = name
        def __getattr__(self, attr):
            name = '.'.join((self.name, attr))
            return Mock(name)
    class HTMLTranslatorWrapper(HTMLTranslator):
        def __init__(self, *args, **kwargs):
            builder = FakeBuilder()
            HTMLTranslator.__init__(self, builder, *args, **kwargs)
    class Writer(BaseWriter):
        def __init__(self, *args, **kwargs):
            BaseWriter.__init__(self, *args, **kwargs)
            self.translator_class = HTMLTranslatorWrapper
except ImportError:  # pragma: no cover
    Writer = BaseWriter

from soho.config import ENCODING
from soho.generators import BaseGenerator


DOCUTILS_SETTINGS = {'strip_comments': True,
                     'output_encoding': ENCODING,
                     'initial_header_level': 2}
META_REGEXP = re.compile('<meta content="(.*?)" name="(.*?)".*?>')


class RSTGenerator(BaseGenerator):

    def generate(self, path):
        with open(path, 'r') as in_file:
            writer = Writer()
            parts = publish_parts(in_file.read(),
                                  writer=writer,
                                  settings_overrides=DOCUTILS_SETTINGS)
        # Read metadata from a '.meta.py' file it one exists
        meta = self._read_metadata_from_file(path)
        # And update (or create) from metadata embedded in the source
        # file itself.
        for value, key in META_REGEXP.findall(parts['meta']):
            meta[key] = value
        return meta, parts['body'].strip()


ReSTGenerator = RSTGenerator  # </pedantic>
