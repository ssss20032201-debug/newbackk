import os
import sys

# yourusername — o'zingizning PythonAnywhere username bilan almashtiring
path = '/home/yourusername/backedim'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'backedim.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
    