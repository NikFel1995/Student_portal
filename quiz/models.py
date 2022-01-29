from django.db import models
from classroom.models import Module
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

import random
from datetime import datetime, timedelta


def get_deadline():
    return datetime.today() + timedelta(days=15)


class Quiz(models.Model):
    module = models.ForeignKey(Module, related_name='quizzes', on_delete=models.CASCADE, verbose_name='Модуль')
    title = models.CharField(max_length=120, verbose_name='Название')
    description = models.TextField(blank=True, help_text='Необязательно к заполнению', verbose_name='Описание')
    # number_of_questions = models.PositiveSmallIntegerField(verbose_name='Количество вопросов')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    due_date = models.DateField(default=get_deadline, verbose_name='Срок выполнения')
    time_limit_min = models.PositiveSmallIntegerField(help_text='в минутах (от 5 до 20)', default=15,
                                                      validators=[MinValueValidator(5), MaxValueValidator(20)],
                                                      verbose_name='Время тестирования')
    allowed_attempts = models.PositiveSmallIntegerField(default=3, help_text='от 1 до 5',
                                                        validators=[MinValueValidator(1), MaxValueValidator(5)],
                                                        verbose_name='Количество попыток')

    def __str__(self):
        return self.title

    def get_questions(self):
        questions_all = list(self.questions.all())
        random.shuffle(questions_all)
        return questions_all

    class Meta:
        verbose_name = 'Тестирование'
        verbose_name_plural = 'Тестирования'
        ordering = ['-created_date']


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE, verbose_name='Опрос')
    title = models.CharField(max_length=300, verbose_name='Вопрос')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    def get_answers(self):
        answers_all = list(self.answers.all().filter(question=self))
        random.shuffle(answers_all)
        return answers_all

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['-created_date']


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE, verbose_name='Вопрос')
    title = models.CharField(max_length=200, verbose_name='Ответ')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ?')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Ответ \'{self.title}\' на вопрос \'{self.question.title}\''

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['-created_date']


class Result(models.Model):
    user = models.ForeignKey(User, related_name='result_received', on_delete=models.CASCADE, verbose_name='Пользователь')
    quiz = models.ForeignKey(Quiz, related_name='results', on_delete=models.CASCADE, verbose_name='Тестирование')
    attempt = models.PositiveSmallIntegerField(verbose_name='Попытка')
    number_of_correct_answers = models.PositiveSmallIntegerField(verbose_name='Количество правильных ответов')
    completed = models.DateTimeField(auto_now_add=True, verbose_name='Дата/время завершения')

    def __str__(self):
        return f'{self.quiz.title} для группы {self.quiz.module.course.group}'

    def get_absolute_url(self):
        return reverse('classroom:quiz:quiz_results', kwargs={'group_id': self.quiz.module.course.group.id,
                                                              'course_id': self.quiz.module.course.id,
                                                              'module_id': self.quiz.module.id,
                                                              'quiz_id': self.quiz.id,
                                                              })

    class Meta:
        verbose_name = 'Результат тестирования'
        verbose_name_plural = 'Результаты тестирования'
        ordering = ['-completed']
