# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from diplom.video.models import Video, Category, Subtitle
from django.contrib import admin


admin.site.register(Category)
admin.site.register(Video)
admin.site.register(Subtitle)