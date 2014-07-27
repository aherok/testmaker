# -*- coding: utf-8 -*-

from django.contrib import admin
from tester.models import Question, Choice, Test


class ChoiceInline(admin.TabularInline):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('test', 'content', 'order')
    list_filter = ('test',)
    inlines = [ChoiceInline]


admin.site.register(Test)
admin.site.register(Question, QuestionAdmin)
