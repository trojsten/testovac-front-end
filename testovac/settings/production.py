from __future__ import absolute_import

from django.core.exceptions import ImproperlyConfigured

from testovac.settings.common import *


def requiredenv(name):
    if name not in os.environ:
        raise ImproperlyConfigured(
            "Value %s missing in environment configuration" % name
        )
    return os.environ.get(name)


SENDFILE_BACKEND = "sendfile.backends.nginx"
SENDFILE_ROOT = "/home/app/web/"
SENDFILE_URL = "/protected-files"


DEBUG = False
SECRET_KEY = requiredenv("TESTOVAC_FRONT_SECRET_KEY")
ALLOWED_HOSTS = requiredenv("TESTOVAC_FRONT_ALLOWED_HOSTS").split(" ")


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp-out.default.svc.cluster.local"
DEFAULT_FROM_EMAIL = "davidb@ksp.sk"
SERVER_EMAIL = "davidb@ksp.sk"
