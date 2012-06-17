from setuptools import setup


# Of course, this is not a real Python package. We use 'setup()' only
# to register message extractors.
setup(packages=(),
      message_extractors={'.': (
            ('src/**meta.py', 'lingua_python', None),
            ('templates/**.pt', 'lingua_xml', None),
            )}
      )
