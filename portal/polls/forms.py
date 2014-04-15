from __future__ import unicode_literals
from django import forms
from portal.polls.models import UserAnswer


class FirstPollForm(forms.ModelForm):

    class Meta:
        model = UserAnswer
        exclude = ('user', )