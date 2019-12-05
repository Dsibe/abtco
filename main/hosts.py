from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'www', 'main.urls', name='www'),
    host(r'', 'main.urls', name='root'),
    host(r'khatynka', 'khatynka.urls', name='khatynka'),
)
