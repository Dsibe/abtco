from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'www.abtco.us', 'main.urls', name='www'),
    host(r'', 'main.urls', name='root'),
    host(r'khatynka', 'khatynka.urls', name='khatynka'),
    host(r'shop', 'shop.urls', name='shop'),
)
