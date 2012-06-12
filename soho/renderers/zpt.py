"""Define the ``ZPTRenderer`` that can render ZPT (Zope Page
Templates).
"""

from chameleon import PageTemplateFile

from soho.config import ENCODING
from soho.renderers import BaseRenderer


class ZPTRenderer(BaseRenderer):
    def __init__(self, filename, translate):
        self.template = PageTemplateFile(
            filename, encoding=ENCODING, translate=translate)

    def render(self, **bindings):
        return self.template.render(**bindings)
