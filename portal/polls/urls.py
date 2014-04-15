from __future__ import unicode_literals
from django.conf.urls import patterns, url
from django.contrib import admin
from portal.user.decorators import login_required
from portal.polls.views.first_poll import FirstPollStart, FirstPollView


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', login_required(FirstPollStart.as_view()), name='first_poll_start'),
    url(r'^dep/$', login_required(FirstPollView.as_view()), name='first_poll'),
)
