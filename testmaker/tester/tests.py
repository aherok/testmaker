# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.test import TestCase

from tester.models import Test, Question, Choice

User = get_user_model()


class UserAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='user@example.com', password='secret')

        self.test = Test.objects.create(name='Some Test')
        self.q1 = Question.objects.create(test=self.test, content='question 1')
        self.c11 = Choice.objects.create(question=self.q1, content='some sophisticated answer', is_correct=True)
        self.c12 = Choice.objects.create(question=self.q1, content='answer2')

    def test_no_access_for_anonymous(self):
        response = self.client.get('/test/1/')
        self.assertEqual(response.status_code, 401)


class TestListViewTests(TestCase):
    def test_no_objects(self):
        self.response = self.client.get('/')
        self.assertTrue('Brak testów' in self.response.content)

    def test_list_view_contains_tests_list(self):
        # create 5 test objects
        [Test.objects.create(name='test nr %s' % i) for i in range(5)]

        self.response = self.client.get('/')

        self.assertTrue('test_list' in self.response.context)
        self.assertEqual(len(self.response.context['test_list']), 5,
                         '`test_list` context var length should equal 5')

    def test_list_view_pagination_by_10(self):
        # create 15 test objects
        [Test.objects.create(name='test nr %s' % i) for i in range(15)]

        self.response = self.client.get('/')

        # tests count
        self.assertEqual(len(self.response.context['test_list']), 10,
                         '`test_list` context var length should be paginated by 10')

        # pagination info
        self.assertTrue('Strona 1 z 2' in self.response.content)


class QuizTestCase(TestCase):
    def test_empty_answer(self):
        """
        Submitting form without form answer should display error
        :return:
        """
        # setup data
        test = Test.objects.create(name='Some Test')

        q1 = Question.objects.create(test=test, content='question 1')
        c11 = Choice.objects.create(question=q1, content='some sophisticated answer', is_correct=True)
        c12 = Choice.objects.create(question=q1, content='answer2')

        # load first step
        response = self.client.get('/test/1/')
        self.assertEqual(response.context['wizard']['steps'].current, "0")

        # POST request
        self.assertTrue('some sophisticated answer' in response.content)
        response = self.client.post('/test/1/', {'test_view-current_step': "0"})

        self.assertEqual(response.context['wizard']['steps'].current, "0")
        self.assertTrue('answer' in response.context['form'].errors)


    def test_correct_step_submission(self):
        """
        First step is passed without errors
        :return:
        """
        # setup data
        test = Test.objects.create(name='Some Test')

        q1 = Question.objects.create(test=test, content='question 1')
        c11 = Choice.objects.create(question=q1, content='some sophisticated answer', is_correct=True)
        c12 = Choice.objects.create(question=q1, content='answer2')
        c13 = Choice.objects.create(question=q1, content='answer3')

        q2 = Question.objects.create(test=test, content='question 2')
        c21 = Choice.objects.create(question=q2, content='answer1', is_correct=True)
        c22 = Choice.objects.create(question=q2, content='answer2')

        # load first step
        response = self.client.get('/test/1/')
        self.assertTrue('some sophisticated answer' in response.content)

        # POST
        response = self.client.post('/test/1/', {'test_view-current_step': "0", 'q-1-answer': unicode(c11.id), })
        self.assertEqual(response.context['wizard']['steps'].current, "1")
        self.assertTrue(not response.context['form'].errors)

    def test_wrong_data(self):
        """
        wrong data is sent through form - should display error message
        :return:
        """
        # setup data
        test = Test.objects.create(name='Some Test')

        q1 = Question.objects.create(test=test, content='question 1')
        c11 = Choice.objects.create(question=q1, content='some sophisticated answer', is_correct=True)
        c12 = Choice.objects.create(question=q1, content='answer2', is_correct=True)
        c13 = Choice.objects.create(question=q1, content='answer3')

        # load first step
        response = self.client.get('/test/1/')
        self.assertTrue('some sophisticated answer' in response.content)

        # POST wrong data
        response = self.client.post('/test/1/',
                                    {'test_view-current_step': "0", 'q-%s-answer' % q1.id: 'wrong data sent', })
        self.assertEqual(response.context['wizard']['steps'].current, "0")
        self.assertTrue('answer' in response.context['form'].errors)


    def test_correct_full_submission(self):
        # setup data
        test = Test.objects.create(name='Some Test')

        q1 = Question.objects.create(test=test, content='question 1')
        c11 = Choice.objects.create(question=q1, content='some sophisticated answer', is_correct=True)
        c12 = Choice.objects.create(question=q1, content='answer2', is_correct=True)
        c13 = Choice.objects.create(question=q1, content='answer3')

        q2 = Question.objects.create(test=test, content='question 2')
        c21 = Choice.objects.create(question=q2, content='answer1', is_correct=True)
        c22 = Choice.objects.create(question=q2, content='answer2')

        # load first step
        response = self.client.get('/test/1/')
        self.assertTrue('some sophisticated answer' in response.content)

        # POST first step - set one correct answer
        response = self.client.post('/test/1/',
                                    {'test_view-current_step': "0", 'q-%s-answer' % q1.id: [c11.id, c13.id], })
        self.assertEqual(response.context['wizard']['steps'].current, "1")
        self.assertTrue(not response.context['form'].errors)

        # POST second step - set one correct answer
        response = self.client.post('/test/1/',
                                    {'test_view-current_step': "1", 'q-%s-answer' % q2.id: c21.id, })
        self.assertTrue('wizard' not in response.context)
        self.assertEqual(response.context['points_count'], 2)

