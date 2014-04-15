from __future__ import unicode_literals
from django.conf.urls import patterns, url
from django.contrib import admin
from django.views.generic import TemplateView
from portal.user.decorators import login_required
from portal.polls.views.first_poll import FirstPollStart, FirstPollView


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='super_site.html'), name='super_site'),
)
