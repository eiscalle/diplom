from __future__ import unicode_literals
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm as AbstractCreationForm
    )
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from portal.user.models import PortalUser


class UserCreationForm(AbstractCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    error_messages = {
        'duplicate_work_email': _("A user with that work email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }

    class Meta(AbstractCreationForm.Meta):
        model = PortalUser

    def clean_work_email(self):
        work_email = self.cleaned_data["work_email"]
        try:
            PortalUser.objects.get(work_email=work_email)
        except ObjectDoesNotExist:
            return work_email
        raise forms.ValidationError(self.error_messages['duplicate_work_email'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = PortalUser
        fields = (
            'personal_email',
            'first_name',
            'last_name',
            'middle_name',
            'mobile_phone',
            'work_phone',
            'skype',
            'birth_date',
            'avatar'
        )


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = PortalUser
        fields = (
            'work_email',
            'personal_email',
            'first_name',
            'last_name',
            'middle_name',
            'leader',
            'mobile_phone',
            'work_phone',
            'skype',
            'placement_date',
            'about',
            'birth_date',
            'is_active',
            'is_admin',
            'is_fabric',
            'tag'
        )
        exclude = ('password', 'avatar')

    def clean_is_admin(self):
        self.instance.is_superuser = True if self.cleaned_data['is_admin'] else False
        return self.cleaned_data['is_admin']
