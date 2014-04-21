# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, url
from diplom.user.views import RegistrationView, AuthView

__author__ = 'sidchik'


urlpatterns = patterns('',
    url(r'^registration/$', RegistrationView.as_view(), name='registration'),
    url(r'^logout/$', 'diplom.user.views.logout_user', name='logout'),
    url(r'^login/$', AuthView.as_view(), name='login'),

)
