from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic.list import ListView
from tester.models import Test

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', ListView.as_view(model=Test, paginate_by=10), name='home'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^', include('tester.urls')),
                       url(r'^', include('accounts.urls')),
)
