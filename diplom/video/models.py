# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from diplom.user.models import DiplomUser
from django.core.urlresolvers import reverse
from django.db import models
from filebrowser.fields import FileBrowseField


class Category(models.Model):
    name = models.CharField('Название категории', default='', max_length=255)

    def get_absolute_url(self):
        return reverse('category_detail', args=[self.pk])

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Video(models.Model):
    name = models.CharField('Название', max_length=255, default='')
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='videos')
    source = FileBrowseField('Видео',
                           directory='videos/',
                           extensions=['.mp4', ],
                           max_length=300,
    )
    is_moderated = models.BooleanField('Отмодерировано', default=False)
    user = models.ForeignKey(DiplomUser, verbose_name='Пользователь', related_name='videos')

    def get_absolute_url(self):
        return reverse('video_detail', args=[self.pk])

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'


class Subtitle(models.Model):
    lang = models.CharField('Язык', default='en', max_length=20, choices=(('ru', 'Русский'), ('en', 'Английский')))
    video = models.ForeignKey(Video, verbose_name='Видео', related_name='subtitles')
    source = FileBrowseField('Субтитры',
                           directory='videos/subtitles/',
                           extensions=['.srt', ],
                           max_length=300,
    )

    def __unicode__(self):
        self.video.name

    class Meta:
        verbose_name = 'Субтитр'
        verbose_name_plural = 'Субтитры'