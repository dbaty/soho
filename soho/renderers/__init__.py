import os


registry = {}


class BaseRenderer(object):
    def __init__(self, template_path):  # pragma: no coverage
        raise NotImplementedError

    def render(self, **bindings):  # pragma: no coverage
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
