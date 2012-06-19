import itertools
import os
from setuptools import find_packages
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(here, 'README.rst')).read()
changes = open(os.path.join(here, 'CHANGES.rst')).read()
requires = ()
extras_require = {'i18n': ('translationstring', ),
                  'rst': ('docutils',
                          'pygments'),
                  'zpt': ('chameleon', )}
all_extras = tuple(itertools.chain(*extras_require.values()))
extras_require['all'] = all_extras
# Sphinx is not required but can be installed to benefit from several
# extra ReST directives it defines.
tests_require = ('mock', 'sphinx') + all_extras


setup(name='Soho',
      version='0.8.0',
      description='A static web site generator',
      long_description='\n\n'.join((readme, changes)),
      classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Text Processing :: Markup :: HTML',
        ),
      author='Damien Baty',
      author_email='damien.baty.remove@gmail.com',
      url='http://readthedocs.org/projects/soho',
      keywords='web static site generator',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      extras_require=extras_require,
      tests_require=tests_require,
      test_suite='tests',
      entry_points='''
      [console_scripts]
      soho-build = soho.cli:main
      ''')
