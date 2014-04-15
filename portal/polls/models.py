# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from portal.user.models import PortalUser
import requests
from app.settings import TAG_RATING_SELF_POLL, TAG_COOPERATION_POLL


class Department(models.Model):
    name = models.CharField('Название отдела', max_length=255, default='')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'


class Question(models.Model):
    text = models.CharField('Текст вопроса', max_length=1000, default='')
    number = models.PositiveSmallIntegerField('Номер вопроса', default=0, unique=True)

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(Question, verbose_name='Вопрос', null=True)
    text = models.CharField('Текст ответа', max_length=1000, default='')
    weight = models.PositiveSmallIntegerField('Вес ответа', default=0)

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class UserAnswer(models.Model):
    user = models.ForeignKey(PortalUser, verbose_name='Ползователь', related_name='user_answers')
    department = models.ForeignKey(Department, verbose_name='Отдел', related_name='user_answers')
    answer = models.ForeignKey(Answer, verbose_name='Ответ', related_name='user_answers')
    created_at = models.DateTimeField('Дата ответа', auto_now_add=True)

    def __unicode__(self):
        return self.user.work_email

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователей'
