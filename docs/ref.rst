=========
Reference
=========

This chapter provides an exhaustive list of all configuration
settings, command-line options and template bindings of Soho. If you
did not do so yet, you may want to have a look at the :ref:`tutorial`
first.


Configuration file settings
===========================

The configuration file (usually named ``sohoconf.py``) is a standard
Python module that may define the following variables:

``asset_dir``
    The directory where assets (images, stylesheets, etc.) live. Must
    be set to ``None`` if no such directory exists.

    Default: ``'./assets'``.

``assets_only``
    If set, process only assets, not source files. This may be useful
    if the only changes are on the CSS, for example.

    Default: ``False``.

``base_url``
    The base URL of the web site. This is used only to generate the
    URLs in the Sitemap. If you want the Sitemap to have valid URLs,
    this variable must be set.

    Default: ``'http://exemple.com/soho/default-base-url'``

``do_nothing``
    If set, no directories nor files are created. This can be useful
    to test a new configuration. Note that you can combine this
    setting with ``force`` (see below): nothing will be created
    either.

    Default: ``False``

``force``
    If set, force the generation of HTML files, even if they have
    already been generated and are up to date. Note that you can
    combine this setting with ``do_nothing`` (see above).

    Default: ``False``

``hide_index_html``
    If set, ``/index.html`` suffixes are removed from:

    - the ``path`` key that is automatically added in the ``md``
      binding passed to the template (see `Template bindings
      (metadata)`_ below);

    - URLs in the Sitemap (if a Sitemap is generated).

    Default: ``True``

``ignore_files``
    A (possibly empty) sequence of regular expressions. If the path of
    a file matches one of these expressions, it will not be processed.

    Default: ``('.*\.DS_Store$', '.*~$')``

``locale_dir``
    The directory where translations are stored. Must be set to
    ``None`` if no such directory exists.

    Default: ``'./locale'``.

``logger_level``
    The minimum level of the messages that will be logged. Must be one
    of ``debug``, ``info``, ``warning`` or ``error``.

    Default: ``'info'``.

``logger_path``
    The path to the log file. If set to ``-`` (a single dash),
    messages will be logged on the standard output. If a path is
    provided, it must be an absolute path.

    Default: ``'-'``

``out_dir``
    The directory where the web site will be generated. This directory
    will be created if it does not exist.

    Default: ``'./www'``

``src_dir``
    The directory where source files live.

    Default: ``'./src'``

``sitemap``
    The name of the Sitemap file. Must be set to ``None`` if you do
    not want such a file to be generated.

    Default: ``'sitemap.xml'``

``template``
    The filename of the template to use. It must not be a relative or
    absolute path to the file (like ``/path/to/templates/layout.pt``)
    but only a filename (``layout.pt``).

``template_dir``
    The directory where templates live.

    Default: ``'./templates'``

.. note::

   All directories (except ``www_dir``) are expected to exist. If you
   do not need the feature, you must set the path to ``None``.

   Also, each directory may be an absolute path or a relative path. If
   it is a relative path and starts with ``./`` (more precisely a dot
   followed by the separator on your operating system), the path is
   supposed to be relative to the directory of the configuration
   file. For example, ``'./www'`` will indicate a directory named
   ``www`` next to the configuration file. If the given path is a
   relative path and does not start with ``./``, then the path will be
   relative to the working directory.

Default values can be found in the ``soho.defaults`` module and reused
in your own configuration file:

.. code-block:: python

   import soho.defaults

   ignore_files = soho.defaults.DEFAULT_IGNORE_FILES + (
       # Sass source files and cache
       'assets/css/src',
       'assets/css/.sass-cache')


Command-line options
====================

``soho-build`` accepts the following command-line options:

``-a``, ``--assets-only``
    See ``assets_only`` setting above.

``-c CONFIG_FILE``
    Use ``CONFIG_FILE`` as the configuration file. By default, Soho
    uses a file named ``sohoconf.py`` in the working directory.

``-d``, ``--dry-run``, ``-do-nothing``
    See ``do_nothing`` setting above.

``-f``, ``--force``
    See ``force`` setting above.

``-h``, ``--help``
    Show all command-line options.

``-v``, ``--version``
    Show the version number.


Template bindings (metadata)
============================

For each source file that is processed, the template receives two
bindings:

``body``
    The HTML fragment as a string.

``md``
    A dictionary that contains the specific metadata of the source
    file (which inherits from the metadata of its directory,
    recursively) plus the following key:

    ``path``
        The URL to the generated file relative to the root of the
        site. It always starts with a ``/``.

        For example, the source file in ``src/foo/bar/file.html``
        would have a path equal to ``/foo/bar/file.html``.