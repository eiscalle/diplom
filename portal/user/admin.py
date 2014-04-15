# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from portal.user.forms import UserCreationForm, UserChangeForm
from portal.user.models import PortalUser


class PortalUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('work_email', 'first_name', 'last_name', 'middle_name', 'is_active', 'is_fabric', 'is_admin')
    list_filter = ('is_active', 'is_fabric', 'is_admin')
    fieldsets = (
        (u'Личная информация', {
            'fields': ('personal_email', 'first_name', 'last_name', 'middle_name', 'mobile_phone', 'about', 'birth_date')
        }),
        (u'Рабочая информация', {
            'fields': ('work_email', 'work_phone', 'skype', 'placement_date', 'leader', 'tag')
        }),
        (u'Права', {
            'fields': ('is_active', 'is_admin', 'is_fabric')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('work_email', 'password1', 'password2')
        }),
    )
    search_fields = ('work_email', 'first_name', 'last_name')
    ordering = ('work_email',)
    raw_id_fields = ('leader',)


class PollAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'owner', 'target', 'created_at', 'completed')
    raw_id_fields = ('owner', 'target', 'type')
    readonly_fields = ('completed',)


class PollTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'content')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'content')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'poll_type', 'order', 'content', 'created_at')
    raw_id_fields = ('poll_type',)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'content', 'created_at')
    raw_id_fields = ('question',)


class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'answer', 'tag', 'created_at')
    raw_id_fields = ('user', 'question', 'answer', 'tag')


admin.site.register(PortalUser, PortalUserAdmin)