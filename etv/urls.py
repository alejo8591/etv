from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from etv import settings
from dajaxice import urls
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from tastypie.api import Api
from users.api.api import UserProfileResource, UserResource


#Api RESTful
user_api_v1 = Api(api_name='user')
user_api_v1.register(UserResource())
user_api_v1.register(UserProfileResource())

admin.autodiscover()
dajaxice_autodiscover()

urlpatterns = patterns('',
       url(r'^elevate/', include(admin.site.urls)),
       (r'^grappelli/', include('grappelli.urls')),
       url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
       url(r'^register/$', 'users.views.registerFranchisee'),
       url(r'^register/confirm/(?P<activation_key>\w+)', 'users.views.confirmFranchisee'),
       (r'^api/', include(user_api_v1.urls)),
       
)
if settings.DEBUG:
    # Serve static files
    urlpatterns += staticfiles_urlpatterns()
    # Serve uploaded files
    urlpatterns += patterns('',
        url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        )