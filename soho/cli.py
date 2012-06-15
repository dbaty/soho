import logging
from argparse import ArgumentParser
import os
import re
import sys

from soho import __version__ as VERSION
from soho import defaults
from soho.builder import Builder
from soho.config import PATH_SETTINGS
from soho.config import REGEXP_SETTINGS


def main():  # pragma: no coverage
    """Read options from the command-line and the configuration file
    and build the site.
    """
    options = parse_args()
    settings = get_settings(options)
    builder = Builder(**settings)
    builder.build()


def parse_args():  # pragma: no coverage
    parser = ArgumentParser(usage='%(prog)s [options]')
    add = parser.add_argument
    add('-v', '--version',
        action='version',
        version='%%(prog)s %s' % VERSION)
    add('-c',
        metavar="CONFIG-FILE",
        help='Use CONFIG-FILE. '
             'Default value is "%s".' % defaults.DEFAULT_CONFIG_FILE,
        default=None,
        dest='config_file')
    add('-f', '--force',
        help='Force all files to be processed, even if source files '
             'are older than generated files.',
        dest='force',
        action='store_true')
    add('-a', '--assets-only',
        help='Process only assets. Useful if only a CSS has changed, '
             'for example',
        dest='assets_only',
        action='store_true')
    add('-d', '--dry-run', '--do-nothing',
        help='Dry run: do not create or copy any file or directory.',
        dest='do_nothing',
        action='store_true')
    return parser.parse_args()


def get_settings(options):
    """Verify and return settings merged from the command-line
    (provided in ``options``) and the configuration file.
    """
    settings = {}
    if options.config_file is not None:
        conf_path = options.config_file
    else:
        conf_path = defaults.DEFAULT_CONFIG_FILE
    conf_path = os.path.abspath(conf_path)
    conf_dir = os.path.dirname(conf_path)
    exit_if_file_absent(conf_path)
    settings = get_settings_from_conf(conf_path)

    # Merge settings from the command-line and the configuration file,
    # and add default settings if needed.
    for option in ('asset_dir',
                   'assets_only',
                   'base_url',
                   'do_nothing',
                   'filters',
                   'force',
                   'hide_index_html',
                   'locale_dir',
                   'ignore_files',
                   'logger_level',
                   'logger_filename',
                   'out_dir',
                   'src_dir',
                   'sitemap',
                   'template',
                   'template_dir'):
        value = getattr(options, option, None)
        if value is not None:
            # Use value provided via the command-line
            settings[option] = value
        elif option not in settings:
            # Use default value for this missing option
            settings[option] = getattr(defaults, 'DEFAULT_' + option.upper())

    # Massage settings.
    for option, value in settings.items():
        if not value:
            continue
        if option in PATH_SETTINGS:
            settings[option] = os.path.expanduser(value)
            # If path starts with './', it means that the path is
            # relative to the configuration file. Otherwise, suppose
            # that it is an absolute path or a path relative to the
            # working directory.
            if settings[option].startswith('.%s' % os.path.sep):
                settings[option] = os.path.join(conf_dir, settings[option])
            settings[option] = os.path.abspath(settings[option])
        elif option in REGEXP_SETTINGS:
            settings[option] = [re.compile(exp) for exp in value]

    settings['logger'] = get_logger(settings.pop('logger_level'),
                                    settings.pop('logger_filename'))

    # Check files and directory existence.
    if not settings['src_dir']:
        sys.exit('The "src_dir" option cannot be empty.')
    for option in ('asset_dir', 'filters', 'locale_dir',
                   'src_dir', 'template_dir'):
        path = settings[option]
        if path is not None:
            exit_if_file_absent(path)

    # Create output directory if it does not exist already.
    if not os.path.exists(settings['out_dir']):
        os.mkdir(settings['out_dir'])
    return settings


def get_settings_from_conf(path):
    """Return settings as a mapping."""
    settings = {}
    with open(path) as fp:
        exec(fp.read(), {}, settings)
    return settings


def exit_if_file_absent(filename):
    if not os.path.exists(filename):
        logging.error('Could not find file or directory: "%s".', filename)
        logging.error('Process has been aborted.')
        sys.exit(1)


def get_logger(level, filename):
    logger = logging.getLogger('Soho')
    level = {'debug': logging.DEBUG,
             'info': logging.INFO,
             'warning': logging.WARNING,
             'error': logging.ERROR}[level.lower()]
    logger.setLevel(level)
    if filename == '-':
        handler = logging.StreamHandler()
    else:
        # Error log file must be absolute, we do not want to guess.
        if os.path.abspath(filename) != filename:
            sys.exit('The path to the log file must be absolute.')
        handler = logging.FileHandler(filename)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


if __name__ == '__main__':
    main()
