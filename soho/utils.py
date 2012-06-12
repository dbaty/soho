import os.path
import logging
import time

from soho.config import METADATA_FILE_SUFFIX


def register_plugin(registry, spec, *keys):
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
        execfile(path, {}, metadata)
    return metadata


def read_file_metadata(file_path):
    path = '%s%s' % (file_path, METADATA_FILE_SUFFIX)
    return _read_metadata_from_file(path)


def read_dir_metadata(dir_path):
    path = os.path.join(dir_path, METADATA_FILE_SUFFIX)
    return _read_metadata_from_file(path)


def hide_index_html_from(path):
    if not path.endswith('index.html'):
        return path
    return path[:-10].rstrip('/')


class SiteMap(object):
    def __init__(self, path, encoding='utf-8'):
        self.encoding = encoding
        self.path = path
        self.urls = []

    def add(self, path, url, change_freq, priority):
        mtime = time.localtime(os.stat(path).st_mtime)
        last_mod = time.strftime('%Y-%m-%d', mtime)
        self.urls.append({'url': url,
                          'last_mod': last_mod,
                          'change_freq': change_freq,
                          'priority': str(priority)})

    def write(self):
        with open(self.path, 'w+') as out:
            out.write('<?xml version="1.0" encoding="%s"?>\n' % self.encoding)
            ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
            out.write('<urlset xmlns="%s">' % ns)
            for url in self.urls:
                out.write('\n'
                          '  <url>\n'
                          '    <loc>%(url)s</loc>\n'
                          '    <lastmod>%(last_mod)s</lastmod>\n'
                          '    <changefreq>%(change_freq)s</changefreq>\n'
                          '    <priority>%(priority)s</priority>\n'
                          '  </url>\n' % url)
            out.write('</urlset>')
