from copy import deepcopy
import os
import shutil

from soho.config import ENCODING
from soho.config import METADATA_FILE_SUFFIX
from soho.generators import get_generator
from soho.i18n import TranslatorWrapper
from soho.renderers import get_renderer
from soho.utils import hide_index_html_from
from soho.utils import read_dir_metadata
from soho.utils import Sitemap


class Builder(object):
    """Driver class."""

    def __init__(self, asset_dir, assets_only, base_url, do_nothing,
                 filters, force, hide_index_html, i18n_dir,
                 ignore_files, logger, out_dir, src_dir, sitemap,
                 template, template_dir):
        """Initialize the builder.

        Arguments must be passed by name only. Their order may change
        in the future.

        ``asset_dir``
            directory where assets (images, stylesheets, etc.) live
            (if any).

        ``assets_only``
            Process only assets. Useful if the only change is on the
            CSS, for example.

        ``base_url``
            Base URL of the web site. This is used only to generate
            the Sitemap.

        ``do_nothing``
            if set, nothing is created: no directory, no files and no
            wheelbarrows (the latter are evil, anyway: you should not
            create wheelbarrows unless you really know what you are
            doing).

        ``filters``
            path to the user defined filters (Python) module.

        ``force``
            if set, force the generation of HTML files, even if they
            have already been generated and are up to date.

        ``hide_index_html``
            if set, ``/index.html`` suffixes are removed from:

            - the ``path`` attribute that is automatically added in the
              ``md`` binding passed to the template;

            - URLs in the Sitemap (if it is generated).

        ``i18n_dir``
            directory where translations are stored (usually a
            directory called ``locale``).

        ``ignore_files``
            a (possibly empty) list of regular expressions. If the
            path of a file matches one of these expressions, it will
            not be processed.

        ``logger``
            the logger to be used. Duh.

        ``out_dir``
            directory where HTML files will be created.

        ``src_dir``
            directory where source files live.

        ``sitemap``
            name of the Sitemap file (usually ``sitemap.xml``) or
            ``None`` if no such file should be generated.

        ``template_dir``
            directory where templates live (if any).
        """
        self.logger = logger
        self._src_dir = os.path.normpath(src_dir)
        self._asset_dir = os.path.normpath(asset_dir)
        self._template_dir = os.path.normpath(template_dir)
        self.load_translations(i18n_dir)
        self._template = template
        self._out_dir = os.path.normpath(out_dir)

        # FIXME: register filters
        #if filters is not None:
        #    module = load_source('user_defined_filters',
        #                         filters)
        #    self._pre_filters = getattr(module, 'pre_filters', ())
        #    self._post_filters = getattr(module, 'post_filters', ())
        #else:
        #    self._pre_filters = ()
        #    self._post_filters = ()
        self._do_nothing = do_nothing
        self._force = force
        self._assets_only = assets_only
        self._ignore_files = ignore_files
        self._hide_index_html = hide_index_html
        if sitemap:
            self._base_url = base_url
            self._sitemap_path = os.path.join(out_dir, sitemap)
            self.sitemap = Sitemap()
        else:
            self.sitemap = None
        self._changed = False

    def load_translations(self, locale_dir):
        self.translators = TranslatorWrapper(locale_dir)

    def translate(self, msgid, domain=None, mapping=None,
                  default=None, context=None):
        """Translate the given ``msgid``.

        ``None`` default values seem to be required by Chameleon,
        which may call 'translate(msgid)' even when translation is not
        requested by the template.
        """
        if context is None:
            return msgid
        locale = context['md']['locale']
        return self.translators.translate(locale, msgid, domain, mapping)

    def build(self):
        if self._do_nothing:
            self.logger.info('Dry run. No files will be harmed, I promise.')
        self.logger.info('Copying assets...')
        self.process_dir(self._asset_dir,
                         self._asset_dir,
                         callback=self.copy_asset,
                         read_metadata=False)
        if not self._assets_only:
            self.logger.info('Building HTML files...')
            self.process_dir(self._src_dir,
                             self._src_dir,
                             callback=self.process_src_file,
                             read_metadata=True,
                             inherited_metadata={})
        if self.sitemap and (self._changed or self._force):
            self.logger.info('Generated Sitemap...')
            if not self._do_nothing:
                with open(self._sitemap_path, 'w+') as out:
                    self.sitemap.write(out)
        self.logger.info('Done.')
        if self._do_nothing:
            self.logger.info('Dry run. No files have been harmed.')

    def process_dir(self, base_dir, dir_path, callback, read_metadata,
                    inherited_metadata=None):
        if read_metadata:
            dir_metadata = deepcopy(inherited_metadata)
            dir_metadata.update(read_dir_metadata(dir_path))
        else:
            dir_metadata = None
        for filename in os.listdir(dir_path):
            path = os.path.join(dir_path, filename)
            relative_path = path[len(base_dir) + 1:]
            if self.ignore_file(relative_path):
                self.logger.debug('Ignoring "%s".', path)
                continue
            if os.path.isdir(path):
                if not self._do_nothing:
                    out_dir_path = os.path.join(self._out_dir, relative_path)
                    if not os.path.exists(out_dir_path):
                        os.mkdir(out_dir_path)
                self.process_dir(base_dir, path, callback, read_metadata,
                                 dir_metadata)
            else:
                callback(path, relative_path, dir_metadata)

    def copy_asset(self, in_path, relative_path, *_ignored_args):
        out_path = os.path.join(self._out_dir, relative_path)
        if not self.should_overwrite(out_path, in_path):
            self.logger.debug('Not overwriting "%s", it seems up to date.',
                              out_path)
            return
        self.logger.info('Copying "%s" to "%s"' % (in_path, out_path))
        if not self._do_nothing:
            shutil.copy2(in_path, out_path)

    def process_src_file(self, in_path, relative_path, dir_metadata):
        out_path = os.path.join(self._out_dir, relative_path)
        relative_url = relative_path.replace(os.sep, '/')
        if self._hide_index_html:
            relative_url = hide_index_html_from(relative_url)
        if relative_url[0] != '/':
            relative_url = '/%s' % relative_url
        if self.sitemap:
            url = self._base_url + relative_url
            self.sitemap.add(in_path, url, 'monthly', 0.5)
        if not self.should_overwrite(out_path, in_path):
            self.logger.debug('Not overwriting "%s", it seems up to date.',
                              out_path)
            return
        self._changed = True
        self.logger.info('Processing "%s" (writing in "%s").',
                         in_path, out_path)
        generator = get_generator(in_path)
        if generator is None:
            self.logger.info('Could not find any generator for "%s", '
                             'copying it as is.', in_path)
            if not self._do_nothing:
                shutil.copy2(in_path, out_path)
            return 1
        # FIXME: enable pre filters
        #for filter in self._pre_filters:
        #    source = filter(source)
        metadata = deepcopy(dir_metadata)
        file_metadata, body = generator.generate(in_path)
        metadata.update(file_metadata)
        metadata.update(path=relative_url)
        template_path = os.path.join(self._template_dir, self._template)
        renderer = get_renderer(template_path, self.translate)
        bindings = {'body': body,
                    'md': metadata,
                    'assets': '/assets'}
        html_output = renderer.render(**bindings)
        # FIXME: enable post filters
        #for filter in self._post_filters:
        #    content = filter(html_output)
        if not self._do_nothing:
            with open(out_path, 'wb+') as out:
                out.write(html_output.encode(ENCODING))

    def ignore_file(self, relative_path):
        if relative_path.endswith(METADATA_FILE_SUFFIX):
            return True
        for regexp in self._ignore_files:
            if regexp.match(relative_path):
                return True
        return False

    def should_overwrite(self, out_path, in_path):
        return self._force or \
            not os.path.exists(out_path) or \
            os.stat(in_path).st_mtime > os.stat(out_path).st_mtime
