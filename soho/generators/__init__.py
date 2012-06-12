import os
from soho.utils import read_file_metadata


registry = {}


class BaseGenerator(object):

    def read_metadata_from_file(self, path):
        return read_file_metadata(path)

    def generate(self, path):
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
