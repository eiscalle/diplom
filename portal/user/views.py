# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView
from filebrowser.base import FileObject
from portal.user.forms import UserProfileForm
from portal.user.models import PortalUser


class ProfileEditView(UpdateView):
    form_class = UserProfileForm
    template_name = 'portal/profile/edit.html'
    model = PortalUser

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.request.user.pk)

    def form_valid(self, form):
        if 'avatar' in form.changed_data and self.request.user.avatar:
            FileObject(self.request.user.avatar.path).delete()
        form.save()
        return redirect('main')

    def form_invalid(self, form):
        return redirect('main')


class ProfileView(DetailView):
    model = PortalUser
    template_name = 'portal/profile/main.html'

    def get_object(self, queryset=None):
        if not self.kwargs.get(self.pk_url_kwarg, None):
            return self.model.objects.get(pk=self.request.user.pk)
        return super(ProfileView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        return context

