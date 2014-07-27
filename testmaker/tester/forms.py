# -*- coding: utf-8 -*-
from django import forms


class QuestionForm(forms.Form):
    answer = forms.MultipleChoiceField(label="", required=True, widget=forms.CheckboxSelectMultiple())

    def __init__(self, question, *args, **kwargs):
        self.question = question

        kwargs['prefix'] = u"q-%s" % question.id
        super(QuestionForm, self).__init__(*args, **kwargs)

        self.fields['answer'].choices = self.question.choice_set.values_list('id', 'content')
