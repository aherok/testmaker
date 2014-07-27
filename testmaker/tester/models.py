# -*- coding: utf-8 -*-

from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Question(models.Model):
    test = models.ForeignKey(Test)
    content = models.TextField()
    order = models.SmallIntegerField(default=0)

    def __unicode__(self):
        return self.content


class Choice(models.Model):
    question = models.ForeignKey(Question)
    content = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __unicode__(self):
        return self.content
