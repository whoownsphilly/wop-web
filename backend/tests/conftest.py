import os
import django
def pytest_configure():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
    django.setup()
