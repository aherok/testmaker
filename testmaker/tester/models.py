# -*- coding: utf-8 -*-
from django.db import models


class Test(models.Model):
    name = models.CharField(u"Nazwa", max_length=255)
    order = models.SmallIntegerField(u"Kolejność", default=0)

    class Meta:
        ordering = ['order']
        verbose_name = u"Test"
        verbose_name_plural = u"Testy"

    def __unicode__(self):
        return self.name


class Question(models.Model):
    test = models.ForeignKey(Test)
    content = models.TextField(u"Treść")
    order = models.SmallIntegerField(u"Kolejność", default=0)

    class Meta:
        ordering = ['order']
        verbose_name = u"Pytanie"
        verbose_name_plural = u"Pytania"

    def __unicode__(self):
        return self.content

    def check_answers(self, answer_list):
        """
        simple checking - fetch given answer IDs and check how many of them are correct
        :param answer_list: list of answer IDs to check
        :return: number of correct answers
        """
        answer_list = [int(i) for i in answer_list]
        all_answers = self.choice_set.all().values('id', 'is_correct')
        points = 0

        for a in all_answers:
            if a['is_correct']:
                points += (1 if a['id'] in answer_list else -1)
            elif not a['is_correct'] and a['id'] in answer_list:
                points -= 1

        return points


class Choice(models.Model):
    question = models.ForeignKey(Question, verbose_name=u"Pytanie")
    content = models.CharField(u"Treść", max_length=255)
    is_correct = models.BooleanField(u"Odpowiedź poprawna", default=False)

    def __unicode__(self):
        return self.content

    class Meta:
        verbose_name = u"Odpowiedź"
        verbose_name_plural = u"Odpowiedzi"