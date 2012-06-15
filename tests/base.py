from collections import namedtuple


def make_options(**options):
    all_options = {'config_file': None,
                   'force': False,
                   'assets_only': False,
                   'do_nothing': False}
    klass = namedtuple('Options', all_options.keys())
    all_options.update(options)
    return klass(**all_options)
