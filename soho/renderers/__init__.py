import os
from soho.utils import register_plugin


registry = {}


def register_renderer(spec, *ext):
    """Register a renderer.

    ``spec``

        a string that represents the full path to a class, for example
        ``'soho.renderers.zpt.ZPTRenderer'``. The class must implement
        the same interface as :class:`soho.renderers.BaseRenderer`.

    ``ext``
        one or more file extensions to which the plugin will be
        associated. At least one file extension must be provided. File
        extensions should not contain the dot, for example ``'html'``,
        not ``'.html'``.
    """
    register_plugin(registry, spec, *ext)


class BaseRenderer(object):
    """The base class that any renderer must implement.

    There is only one renderer for now, so the API is subject to
    change (as soon as a second renderer is implemented).
    """

    def __init__(self, template_path):  # pragma: no coverage
        raise NotImplementedError

    def render(self, **bindings):  # pragma: no coverage
        """Render the template with the given ``bindings``."""
        raise NotImplementedError


def get_renderer(path, *args, **kwargs):
    """Return a renderer for the given template, or ``None`` if none
    could be found.
    """
    ext = os.path.splitext(path)[1][1:]
    klass = registry.get(ext, None)
    if klass is None:
        return None
    return klass(path, *args, **kwargs)
