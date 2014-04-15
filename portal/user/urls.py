from __future__ import unicode_literals
from django.conf.urls import patterns, url
from django.contrib import admin
from django.views.generic import RedirectView
from portal.user.decorators import login_required
from portal.user.views import ProfileView, ProfileEditView


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', RedirectView.as_view(url='profile/'), name='main'),
    url(r'^profile(?:/(?P<pk>\d+))?/$', login_required(ProfileView.as_view()), name='profile_main'),
    url(r'^profile/edit$', login_required(ProfileEditView.as_view()), name='profile_edit'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'portal/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login/'}, name='logout'),
)
