import os.path
import logging
import time

from soho.config import METADATA_FILE_SUFFIX


def register_plugin(registry, spec, *keys):
    """Register a plugin.

    ``registry``
        should be a Soho registry, i.e. either
        ``soho.generators.registry`` or ``soho.renderers.registry``
        depending on the type of plugin you want to register.

    ``spec``
        the full path to a class, e.g.
        ``'soho.renderers.zpt.ZPTRenderer'``. The class must implement
        the same interface as ``soho.renderers.BaseRenderer`` or
        ``soho.generators.BaseGenerator``.

    ``keys``
        one or more keys under which the plugin will be registered. At
        least one key must be provided. Currently, each key is
        supposed to be a file extension (without the dot, for example
        ``'html'``).

    This function is not part of the API. You should use
    ``soho.generator.register_generator()`` or
    ``soho.renderers.register_renderer()`` instead.
    """
    if not keys:
        raise ValueError('You must provide at least one key to '
                         'register a plugin to.')
    module, klass = spec.rsplit('.', 1)
    try:
        plugin = __import__(module)
        for component in spec.split('.')[1:]:
            plugin = getattr(plugin, component)
        for key in keys:
            registry[key] = plugin
    except ImportError:
        logging.debug('Could not import plugin: "%s".', spec)


def _read_metadata_from_file(path):
    metadata = {}
    if os.path.exists(path):
        with open(path) as fp:
            exec(fp.read(), {}, metadata)
    return metadata


def read_file_metadata(file_path):
    """Return metadata associated to the given file (if any)."""
    path = '%s%s' % (file_path, METADATA_FILE_SUFFIX)
    return _read_metadata_from_file(path)


def read_dir_metadata(dir_path):
    """Return metadata associated to the given directory (if any)."""
    path = os.path.join(dir_path, METADATA_FILE_SUFFIX)
    return _read_metadata_from_file(path)


def hide_index_html_from(path):
    """Remove ``index.html`` suffix as well as trailing slashes (if
    any).
    """
    if not path.endswith('index.html'):
        return path
    return path[:-10].rstrip('/')


class Sitemap(object):
    """A class that can generate Sitemap files.

    See `<http://www.sitemaps.org/>`_ for further details about the
    format of the file.
    """

    def __init__(self):
        self.urls = []

    def add(self, path, url, change_freq, priority):
        """Add a URL to the Sitemap."""
        mtime = time.localtime(os.stat(path).st_mtime)
        last_mod = time.strftime('%Y-%m-%d', mtime)
        self.urls.append({'url': url,
                          'last_mod': last_mod,
                          'change_freq': change_freq,
                          'priority': str(priority)})

    def write(self, out):
        """Write the Sitemap to the given ``out`` stream."""
        out.write('<?xml version="1.0" encoding="utf-8"?>\n')
        ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
        out.write('<urlset xmlns="%s">' % ns)
        for url in sorted(self.urls, key=lambda a: a['url']):
            out.write('\n'
                      '  <url>\n'
                      '    <loc>%(url)s</loc>\n'
                      '    <lastmod>%(last_mod)s</lastmod>\n'
                      '    <changefreq>%(change_freq)s</changefreq>\n'
                      '    <priority>%(priority)s</priority>\n'
                      '  </url>\n' % url)
        out.write('</urlset>')
