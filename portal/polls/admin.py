# -*- coding: utf-8 -*-
from django.contrib import admin
from portal.polls.models import Answer, UserAnswer, Question, Department

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'question', 'weight',)
    list_filter = ('question', )


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'number',)
    ordering = ('number', )



class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'answer', 'department',)
    list_filter = ('user', 'department')


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Department)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)