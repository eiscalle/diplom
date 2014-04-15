# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import requests
from app.settings import TAG_RATING_SELF_POLL, TAG_COOPERATION_POLL


class PortalUserManager(BaseUserManager):
    def create_user(self, work_email=None, password=None):
        user = self.model(work_email=work_email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, work_email, password):
        user = self.create_user(work_email, password)
        user.is_admin = True
        user.is_fabric = False
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Tag(models.Model):
    tag = models.CharField('Тэг', max_length=256)
    content = models.CharField('Название', max_length=256)

    class Meta:
        verbose_name = 'Тэг (отдел фирмы)'
        verbose_name_plural = 'Тэги (отделы фирмы)'

    def __unicode__(self):
        return self.content


class PortalUser(AbstractBaseUser, PermissionsMixin):
    work_email = models.EmailField('Рабочий email', max_length=256, unique=True, db_index=True)
    personal_email = models.EmailField('Личный email', max_length=256, blank=True)
    first_name = models.CharField('Имя', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=30, blank=True)
    middle_name = models.CharField('Отчество', max_length=30, blank=True)
    avatar = models.ImageField('Аватар', max_length=256, upload_to='avatar/', blank=True, null=True)
    leader = models.ForeignKey('self', null=True, blank=True, verbose_name='Начальник')
    mobile_phone = models.CharField('Мобильный телефон', max_length=15, blank=True)
    work_phone = models.CharField('Рабочий телефон', max_length=18, blank=True)
    skype = models.CharField('Skype', max_length=32, blank=True)
    placement_date = models.DateField('Дата устройства в Ailove', null=True, blank=True)
    about = models.TextField('О себе', blank=True)
    birth_date = models.DateField('День рождения', null=True, blank=True)
    is_active = models.BooleanField('Активен', default=True)
    is_admin = models.BooleanField('Права администратора', default=False)
    is_fabric = models.BooleanField('Пользователь из Factory', default=True)
    tag = models.ManyToManyField(Tag, related_name='tag_user', verbose_name='Тэги', null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_staff(self):
        return self.is_admin

    def get_full_name(self):
        return '{1} {2} {3}'.format(self.first_name, self.last_name, self.middle_name)

    def get_short_name(self):
        return self.work_email

    @staticmethod
    def check_fabric_auth(work_email, password):
        username = work_email.split('@')[0]
        response = requests.get('https://factory.ailove.ru/users/current.json', auth=(username, password))
        try:
            response = response.json()
            return response['user'] if work_email == response['user']['mail'] else False
        except ValueError:
            return False

    USERNAME_FIELD = 'work_email'
    REQUIRED_FIELDS = []

    objects = PortalUserManager()
