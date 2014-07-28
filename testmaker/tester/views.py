# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.template.context import Context
from django.template.loader import get_template
from django.template.response import TemplateResponse
from django.utils.datastructures import SortedDict
from django.utils.decorators import method_decorator

from tester.forms import QuestionForm
from tester.models import Test


class TestView(SessionWizardView):
    template_name = 'tester/test_detail.html'

    @method_decorator(login_required)
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
            'points_count': points_count,
            'user': self.request.user,
        }

        # send email if email provided
        if self.request.user.email:
            tpl = get_template('tester/email.txt')
            content = tpl.render(Context(ctx))
            send_mail(u"Twój wynik z TestMakera", content, None, [self.request.user.email])

        return TemplateResponse(self.request, template='tester/test_done.html', context=ctx)
