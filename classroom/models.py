import os

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Group(models.Model):
    title = models.CharField(max_length=100, verbose_name='Группа')
    slug = models.SlugField(db_index=True, unique=True, help_text='Адрес страницы', verbose_name='ЧПУ')
    description = models.TextField(blank=True, help_text='Необязательно к заполнению', verbose_name='Описание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    students = models.ManyToManyField(User, related_name='group_joined', verbose_name='Студенты')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        # ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('classroom:group_detail', kwargs={'group_id': self.id})


class Course(models.Model):
    owner = models.ForeignKey(User, related_name='course_created', on_delete=models.PROTECT, verbose_name='Автор курса')
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, help_text='Адрес страницы', verbose_name='ЧПУ')
    description = models.TextField(blank=True, help_text='Необязательно к заполнению', verbose_name='Описание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    group = models.ForeignKey(Group, related_name='courses_joined', on_delete=models.PROTECT, verbose_name='Группа')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        # ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('classroom:course_detail', kwargs={'group_id': self.group.id, 'course_id': self.id})


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE, verbose_name='Курс')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, help_text='Необязательно к заполнению', verbose_name='Описание')
    hours = models.PositiveSmallIntegerField(verbose_name='Количество часов')

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'
        # ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('classroom:module_detail', kwargs={'group_id': self.course.group.id, 'course_id': self.course.id, 'module_id': self.id})


def user_directory_path(instance, filename):
    # print(instance.module.course.group.all())
    if instance.user == instance.module.course.owner:  # если автор загрузки файла, автор курса
        return f'files/{instance.user.username}/' \
               f'{instance.module.course.group.title}/' \
               f'{instance.module.course.title}/' \
               f'{instance.module.title}/{filename}'
    else:  # иначе автор загрузки файла - участник курса
        return f'files/{instance.user.username}/{filename}'


class Content(models.Model):
    user = models.ForeignKey(User, related_name='content_created', on_delete=models.CASCADE, verbose_name='Пользователь')
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE, verbose_name='Модуль')
    title = models.CharField(max_length=250, verbose_name='Название')
    description = models.TextField(blank=True, help_text='Необязательно к заполнению', verbose_name='Описание')
    file = models.FileField(upload_to=user_directory_path, verbose_name='Файл')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.title

    def get_file_name(self):
        return os.path.basename(self.file.name)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ['created']
