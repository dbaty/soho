import soho.defaults

base_url = 'http://exemple.com'
template = 'layout.pt'
ignore_files = soho.defaults.DEFAULT_IGNORE_FILES + (
    '.*ignored.txt$',
    )
