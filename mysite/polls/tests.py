import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_past_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        past_question = Question(pub_date=time)

        self.assertIs(past_question.was_published_recently(), False)

    def test_was_published_recently_with_recently_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=58)
        recently_question = Question(pub_date=time)

        self.assertIs(recently_question.was_published_recently(), True)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)

    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['question_list'], [])

    def test_no_choice_question(self):
        create_question(question_text='No choice question', days=-1)

        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(response.context['question_list'], [])

    def test_question_with_choice(self):
        question_with_choice = create_question(question_text='With choice question', days=-1)
        question_with_choice.choice_set.create(choice_text='First Choice', votes=0)

        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(response.context['question_list'], ['<Question: With choice question>'])

    def test_past_question_with_choice(self):
        past_question_with_choice = create_question(question_text='Past question.', days=-30)
        past_question_with_choice.choice_set.create(choice_text='First Choice', votes=0)

        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question_with_choice(self):
        future_question_with_choice = create_question(question_text="Future question.", days=30)
        future_question_with_choice.choice_set.create(choice_text='First Choice', votes=0)

        response = self.client.get(reverse('polls:index'))

        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['question_list'], [])

    def test_future_and_past_question_with_choice(self):
        future_question_with_choice = create_question(question_text='Future question.', days=1)
        future_question_with_choice.choice_set.create(choice_text='First Choice', votes=0)
        past_question_with_choice = create_question(question_text='Past question.', days=-30)
        past_question_with_choice.choice_set.create(choice_text='First Choice', votes=0)

        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_question_with_choice(self):
        past_question_1_with_choice = create_question(question_text='Past question 1.', days=-30)
        past_question_1_with_choice.choice_set.create(choice_text='First Choice', votes=0)
        past_question_2_with_choice = create_question(question_text='Past question 2.', days=-80)
        past_question_2_with_choice.choice_set.create(choice_text='First Choice', votes=0)

        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['question_list'],
            ['<Question: Past question 1.>', '<Question: Past question 2.>']
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text='Future question.', days=1)

        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text='Future question.', days=-1)

        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)

        self.assertContains(response, past_question.question_text)


class QuestionVoteViewTests(TestCase):
    def test_undefined_pk_question(self):
        url = reverse('polls:vote', args=(1,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    # TODO ADD FORM POST TEST


