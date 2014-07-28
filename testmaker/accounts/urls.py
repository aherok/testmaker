from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from accounts.views import MyRegistrationView


urlpatterns = patterns('',
                       # auth urls
                       url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

                       # registration urls
                       url(r'^register/$',
                           MyRegistrationView.as_view(),
                           name='registration_register'),
                       url(r'^register/closed/$',
                           TemplateView.as_view(template_name='registration/registration_closed.html'),
                           name='registration_disallowed'),
                       (r'', include('registration.auth_urls')),
)
