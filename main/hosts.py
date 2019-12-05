from django.conf import settings
from django_hosts import patterns, hosthost_patterns = patterns(
    '',
    host(r'www', 'main.urls.py', name='www'),
    host(r'', 'main.urls.py', name='root'),
    host(r'khatynka', 'khatynka.urls.py', name='khatynka'),
)
