from copy import deepcopy
import os
import shutil

from soho.config import ENCODING
from soho.config import METADATA_FILE_SUFFIX
from soho.generators import get_generator
from soho.i18n import interpolate
from soho.i18n import TranslatorWrapper
from soho.renderers import get_renderer
from soho.utils import hide_index_html_from
from soho.utils import read_dir_metadata
from soho.utils import Sitemap


class Builder(object):
    """Driver class."""

    def __init__(self, asset_dir, assets_only, base_url, do_nothing,
                 force, hide_index_html, locale_dir, ignore_files,
                 logger, out_dir, src_dir, sitemap, template,
                 template_dir):
        """Initialize the builder.

        Arguments must be passed by name only. Their order may change
        in the future.

        ``asset_dir``
            The directory where assets (images, stylesheets, etc.)
            live. Must be set to ``None`` if no such directory exists.

        ``assets_only``
            If set, process only assets, not source files. This may be
            useful if the only changes are on the CSS, for example.

        ``base_url``
            The base URL of the web site. This is used only to
            generate the URLs in the Sitemap. If you want the Sitemap
            to have valid URLs, this variable must be set.

        ``do_nothing``
            If set, no directories nor files are created. This can be
            useful to test a new configuration. Note that you can
            combine this setting with ``force`` (see below): nothing
            will be created either.

        ``force``
            If set, force the generation of HTML files, even if they
            have already been generated and are up to date. Note that
            you can combine this setting with ``do_nothing`` (see
            above).

        ``hide_index_html``
            If set, ``/index.html`` suffixes are removed from:

              - the ``path`` key that is automatically added in the
                ``md`` binding passed to the template;

              - URLs in the Sitemap (if a Sitemap is generated).

        ``ignore_files``
            A (possibly empty) sequence of regular expressions. If the
            path of a file matches one of these expressions, it will
            not be processed.

        ``locale_dir``
            The directory where translations are stored. Must be set
            to ``None`` if no such directory exists.

        ``logger``
            The logger to be used.

        ``out_dir``
            The directory where the web site will be generated. This
            directory will be created if it does not exist.

        ``src_dir``
            The directory where source files live.

        ``sitemap``
            The name of the Sitemap file. Must be set to ``None`` if
            you do not want such a file to be generated.

        ``template``
            The filename of the template to use. It must not be a
            relative or absolute path to the file (like
            ``/path/to/templates/layout.pt``) but only a filename
            (``layout.pt``).

        ``template_dir``
            The directory where templates live.
        """
        self.logger = logger
        self._src_dir = src_dir
        self._asset_dir = asset_dir
        self._template_dir = template_dir
        if locale_dir:
            self.load_translations(locale_dir)
        self._template = template
        self._out_dir = out_dir
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
            return interpolate(msgid, mapping)
        locale = context['md']['locale']
        return self.translators.translate(locale, msgid, domain, mapping)

    def build(self):
        if self._do_nothing:
            self.logger.info('Dry run. No files will be harmed, I promise.')
        if self._asset_dir:
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
            self.logger.info('Generating Sitemap...')
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
        generator = get_generator(in_path)
        if generator is not None:
            out_path = '%s.html' % os.path.splitext(out_path)[0]
            relative_url = '%s.html' % os.path.splitext(relative_url)[0]
        if self._hide_index_html:
            relative_url = hide_index_html_from(relative_url)
        if not relative_url or relative_url[0] != '/':
            relative_url = '/%s' % relative_url
        if self.sitemap:
            url = self._base_url + relative_url
            self.sitemap.add(in_path, url, 'monthly', 0.5)
        if not self.should_overwrite(out_path, in_path):
            self.logger.debug('Not overwriting "%s", it seems up to date.',
                              out_path)
            return
        self._changed = True
        if generator is None:
            self.logger.info('Could not find any generator for "%s", '
                             'copying it as is.', in_path)
            if not self._do_nothing:
                shutil.copy2(in_path, out_path)
            return 1
        self.logger.info('Processing "%s" (writing in "%s").',
                         in_path, out_path)
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
