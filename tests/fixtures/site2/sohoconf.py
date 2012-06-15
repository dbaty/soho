import soho.defaults

asset_dir = None
base_url = 'http://exemple.com'
locale_dir = None
template = 'layout.pt'
ignore_files = soho.defaults.DEFAULT_IGNORE_FILES + (
    '.*ignored.txt$',
    )
sitemap = None

del soho
