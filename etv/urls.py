from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from etv import settings
from dajaxice import urls
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

admin.autodiscover()
dajaxice_autodiscover()

urlpatterns = patterns('',
       url(r'^admin/', include(admin.site.urls)),
       (r'^grappelli/', include('grappelli.urls')),
       url(r'^register/', 'users.views.register'),
       url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
       
)
if settings.DEBUG:
    # Serve static files
    urlpatterns += staticfiles_urlpatterns()
    # Serve uploaded files
    urlpatterns += patterns('',
        url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        )