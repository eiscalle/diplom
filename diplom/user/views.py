# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from diplom.user.forms import RegistrationForm
from diplom.user.models import DiplomUser
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views.generic import FormView, View, TemplateView


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'registration.html'
    success = False
    request = None

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)

        context['success'] = self.success
        return context

    def form_valid(self, form):
        # Register User

        user = DiplomUser.objects.create_user(
            username=form.cleaned_data['email'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
        )

        auth_user = authenticate(username=user.username, password=form.cleaned_data['password'])
        login(self.request, auth_user)

        redirect_to = '/'

        return HttpResponseRedirect(redirect_to)


class AuthView(TemplateView):
    template_name = 'login.html'
    http_method_names = ['get', 'post']

    def post(self, request, *args, **kwargs):
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me', None)

        auth_user = authenticate(username=username, password=password)
        if auth_user:
            login(request, auth_user)

            if not remember_me:
                request.session.set_expiry(0)

        if request.GET.get('next', ''):
            redirect_to = request.GET.get('next', '')
        else:
            redirect_to = '/'

        redirect_to = redirect_to if redirect_to else '/'


        return HttpResponseRedirect(redirect_to)

def logout_user(request):
    logout(request)
    redirect_to = '/'
    return HttpResponseRedirect(redirect_to)