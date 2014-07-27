# -*- coding: utf-8 -*-

from django.contrib import admin
from tester.models import Question, Choice, Test


class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('test', 'content', 'order')
    list_filter = ('test',)
    inlines = [ChoiceInline]


admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
