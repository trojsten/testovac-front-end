import os

#If having issues with imports, this might help
#import sys
#sys.path.insert(0, '/home/testovac/adhoc/env3/lib/python3.4/site-packages/')

import dotenv

dotenv.read_dotenv()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testovac.settings.production")

identity = os.environ.get("TESTOVAC_FRONT_JUDGE_INTERFACE_IDENTITY")
if identity != 'ZURICH':
    raise ValueError("Wrong env, this should be 'ZURICH': " + identity)

# This might also help
# https://modwsgi.readthedocs.io/en/master/user-guides/reloading-source-code.html
#
# import importlib
# importlib.invalidate_caches()


application = get_wsgi_application()