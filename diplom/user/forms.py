# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from diplom.user.models import DiplomUser
from django import forms


class RegistrationForm(forms.Form):
    email = forms.EmailField(label=u'Эл. почта', max_length=64, required=True)

    password = forms.CharField(label=u'Пароль', max_length=64, required=True, widget=forms.PasswordInput, min_length=5)
    confirm_password = forms.CharField(label=u'Подтверждение пароля', max_length=64, required=True, widget=forms.PasswordInput, min_length=5)

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if not email:
            raise forms.ValidationError(u'Введите email')

        try:
            user = DiplomUser.objects.get(email=email)
        except DiplomUser.DoesNotExist:
            return email

        raise forms.ValidationError(u'Данный email уже существует')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password', '')
        confirm_password = self.cleaned_data.get('confirm_password', '')

        if password != confirm_password:
            raise forms.ValidationError(u'Пароли не совпадают')

        return confirm_password