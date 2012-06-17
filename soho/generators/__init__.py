import os
from soho.utils import read_file_metadata
from soho.utils import register_plugin


registry = {}


def register_generator(spec, *ext):
    """Register a generator.

    ``spec``
        a string that represents the full path to a class, for example
        ``'soho.generators.rst.RSTGenerator'``. The class must
        implement the same interface as
        :class:`soho.generators.BaseGenerator`.

    ``ext``
        one or more file extensions to which the plugin will be
        associated. At least one file extension must be provided. File
        extensions should not contain the dot, for example ``'html'``,
        not ``'.html'``.
    """
    register_plugin(registry, spec, *ext)


class BaseGenerator(object):
    """The base class that any generator must implement."""

    def _read_metadata_from_file(self, path):
        """Return metadata about the file at the given ``path`` by
        reading from a file named ``<path>.meta.py`` if such a file
        exists.
        """
        return read_file_metadata(path)

    def generate(self, path):  # pragma: no coverage
        """Return a tuple that consists of the metadata and the HTML
        fragment generated from the file at the given ``path``.
        """
        raise NotImplementedError


def get_generator(path, *args, **kwargs):
    """Return an instance of the generator for the given file, or
    ``None`` if none could be found.
    """
    ext = os.path.splitext(path)[1][1:]
    klass = registry.get(ext, None)
    if klass is None:
        return None
    return klass(*args, **kwargs)
