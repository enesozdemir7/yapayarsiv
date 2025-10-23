from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'www', settings.ROOT_URLCONF, name='root'), 
    host(r'kurs', 'course.urls', name='course'),
)
