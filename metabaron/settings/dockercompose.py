from .base import *
STATIC_ROOT="/code/static/"
INSTALLED_APPS += (
        'debug_toolbar',
    )

MIDDLEWARE +=(
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
ALLOWED_HOSTS = ['*']
