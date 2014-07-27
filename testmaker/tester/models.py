# -*- coding: utf-8 -*-
from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=255)
    order = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.name


class Question(models.Model):
    test = models.ForeignKey(Test)
    content = models.TextField()
    order = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.content

    def check_answers(self, answer_list):
        """
        simple checking - fetch given answer IDs and check how many of them are correct
        :param answer_list: list of answer IDs to check
        :return: number of correct answers
        """
        return self.choice_set.filter(is_correct=True, id__in=answer_list).count()


class Choice(models.Model):
    question = models.ForeignKey(Question)
    content = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __unicode__(self):
        return self.content
