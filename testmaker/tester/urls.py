from django.conf.urls import patterns, include, url

from django.views.generic.list import ListView
from tester.models import Test


urlpatterns = patterns('',
                       url(r'^$', ListView.as_view(model=Test, paginate_by=10), name='home'),
)
