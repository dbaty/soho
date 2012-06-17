"""Define the ``HTMLGenerator``, which takes HTML as input and return
the same HTML as output.
"""

from soho.generators import BaseGenerator


class HTMLGenerator(BaseGenerator):

    def generate(self, path):
        meta = self._read_metadata_from_file(path)
        with open(path, 'r') as in_file:
            return meta, in_file.read()
