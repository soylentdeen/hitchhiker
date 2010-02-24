
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns( '',

)

if getattr( settings, 'STATIC_SERVE_LOCALLY', False ):
    urlpatterns += patterns( 'django.views',
        url( r'^%s(?P<path>.*)$' % settings.STATIC_URL[ 1: ], 'static.serve', { 'document_root': settings.STATIC_ROOT } ),
        url( r'^%s(?P<path>.*)$' % settings.MEDIA_URL[ 1: ], 'static.serve', { 'document_root': settings.MEDIA_ROOT } ),
    )

