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
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/login/' in response.url)


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
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='user@example.com', password='secret')
        self.client.login(username='test_user', password='secret')

        self.test = Test.objects.create(name='Some Test')
        self.test_url = '/test/%s/' % self.test.id

        self.q1 = Question.objects.create(test=self.test, content='question 1')
        self.c11 = Choice.objects.create(question=self.q1, content='some sophisticated answer', is_correct=True)
        self.c12 = Choice.objects.create(question=self.q1, content='answer2', is_correct=True)
        self.c13 = Choice.objects.create(question=self.q1, content='answer3')

        self.q2 = Question.objects.create(test=self.test, content='question 2')
        self.c21 = Choice.objects.create(question=self.q2, content='answer1', is_correct=True)
        self.c22 = Choice.objects.create(question=self.q2, content='answer2')

    def test_empty_answer(self):
        """
        Submitting form without form answer should display error
        :return:
        """
        # load first step
        response = self.client.get(self.test_url)
        self.assertTrue('Some Test' in response.content)
        self.assertEqual(response.context['wizard']['steps'].current, "0")

        # POST request
        self.assertTrue('some sophisticated answer' in response.content)
        response = self.client.post(self.test_url, {'test_view-current_step': "0"})

        self.assertEqual(response.context['wizard']['steps'].current, "0")
        self.assertTrue('answer' in response.context['form'].errors)


    def test_correct_step_submission(self):
        """
        First step is passed without errors
        :return:
        """
        # load first step
        response = self.client.get(self.test_url)
        self.assertTrue('some sophisticated answer' in response.content)

        # POST
        response = self.client.post(self.test_url,
                                    {'test_view-current_step': "0", 'q-1-answer': unicode(self.c11.id), })
        self.assertEqual(response.context['wizard']['steps'].current, "1")
        self.assertTrue(not response.context['form'].errors)

    def test_wrong_data(self):
        """
        wrong data is sent through form - should display error message
        :return:
        """
        # load first step
        response = self.client.get(self.test_url)
        self.assertTrue('some sophisticated answer' in response.content)

        # POST wrong data
        response = self.client.post(self.test_url,
                                    {'test_view-current_step': "0", 'q-%s-answer' % self.q1.id: 'wrong data sent', })
        self.assertEqual(response.context['wizard']['steps'].current, "0")
        self.assertTrue('answer' in response.context['form'].errors)


    def test_correct_full_submission(self):
        # load first step
        response = self.client.get(self.test_url)
        self.assertTrue('some sophisticated answer' in response.content)

        # POST first step - set one correct answer
        response = self.client.post(self.test_url,
                                    {'test_view-current_step': "0",
                                     'q-%s-answer' % self.q1.id: [self.c11.id, self.c13.id], })
        self.assertEqual(response.context['wizard']['steps'].current, "1")
        self.assertTrue(not response.context['form'].errors)

        # POST second step - set one correct answer
        response = self.client.post(self.test_url,
                                    {'test_view-current_step': "1", 'q-%s-answer' % self.q2.id: self.c21.id, })
        self.assertTrue('wizard' not in response.context)
        self.assertTrue('points_count' in response.context)

    def test_all_correct_answers(self):
        # 2 / 2 correct answers = 2 points
        self.assertEqual(self.q1.check_answers([self.c11.id, self.c12.id]), 2)

        # 1 / 2 correct answers = 0 points
        self.assertEqual(self.q1.check_answers([self.c11.id]), 0)

        # 1 / 2 correct answers and 1 bad = -1 points
        self.assertEqual(self.q1.check_answers([self.c11.id, self.c13.id]), -1)

