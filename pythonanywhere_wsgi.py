"""
PythonAnywhere WSGI konfiguratsiyasi.
Bu faylni PythonAnywhere Web tab > WSGI configuration file'ga ko'chiring.
"""
import os
import sys

# Proyekt papkasining to'liq yo'lini ko'rsating
path = '/home/yourusername/backedim'
if path not in sys.path:
    sys.path.insert(0, path)
    




os.environ['DJANGO_SETTINGS_MODULE'] = 'backedim.settings'
#cdcdcd

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
