__version__ = '0.8.0'

import soho.generators
import soho.renderers
from soho.utils import register_plugin

register_plugin(soho.generators.registry,
                'soho.generators.html.HTMLGenerator',
                'html', 'zpt', 'pt')
# FIXME: register ReST generator


register_plugin(soho.renderers.registry,
                'soho.renderers.zpt.ZPTRenderer',
                'html', 'zpt', 'pt')
