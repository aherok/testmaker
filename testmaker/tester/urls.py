from django.conf.urls import patterns, include, url

from tester.forms import QuestionForm
from tester.views import TestView


urlpatterns = patterns('',
                       url(r'^test/(?P<pk>\d+)/$', TestView.as_view([QuestionForm]), name='test_detail'),
)
