# -*- coding: utf-8 -*-
from django.contrib.formtools.wizard.views import SessionWizardView
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.datastructures import SortedDict

from tester.forms import QuestionForm
from tester.models import Test


class TestView(SessionWizardView):
    template_name = 'tester/test_detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.test = get_object_or_404(Test.objects.select_related('question_set', 'question__choice_set'),
                                      pk=self.kwargs.get('pk'))

        # override self.form_list so it is created dynamically based on given self.test instance
        self.form_list = SortedDict()
        for k in range(self.test.question_set.count()):
            self.form_list[unicode(k)] = QuestionForm
        return super(TestView, self).dispatch(request, *args, **kwargs)

    def get_form(self, step=None, data=None, files=None):
        if step is None:
            step = self.steps.current

        question = self.test.question_set.all()[int(step)]
        form = QuestionForm(question=question, data=data, files=files)
        return form

    def get_context_data(self, form, **kwargs):
        ctx = super(TestView, self).get_context_data(form, **kwargs)
        ctx.update({
            'test': self.test
        })
        return ctx

    def done(self, form_list, **kwargs):
        points_count = 0
        for form in form_list:
            answers = form.cleaned_data.get('answer')
            points_count += form.question.check_answers(answers)

        ctx = {
            'test': self.test,
            'points_count': points_count
        }
        return TemplateResponse(self.request, template='tester/test_done.html', context=ctx)
