from hkbattery.settings.base import *


DEBUG = False

ALLOWED_HOSTS = ['*']
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')


# Use the cached template loader so template is compiled once and read from
# memory instead of reading from disk on each load.
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]
