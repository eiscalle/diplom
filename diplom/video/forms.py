# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from diplom.video.models import Video
from django import forms
from filebrowser.fields import FileBrowseFormField
from filebrowser.widgets import FileInput


class VideoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(VideoForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            if type(self.fields[field_name]) is FileBrowseFormField:
                self.fields[field_name].widget = FileInput()


    class Meta:
        model = Video
        exclude = ('user', 'is_moderated')