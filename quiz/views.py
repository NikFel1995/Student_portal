from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Quiz, Question, Answer, Result
from classroom.models import Course, Group, Module
import datetime


@login_required
def quizView(request, group_id, course_id, module_id, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quiz, id=quiz_id)
    group = get_object_or_404(Group, id=group_id)
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    questions = quiz.get_questions()
    users_in_group = User.objects.filter(group_joined=group)  # список студентов в группе
    context = {}
    if user in users_in_group:
        context = {'quiz': quiz, 'questions': questions, 'group': group, 'course': course, 'module': module}
    context['user_in_group'] = user in users_in_group
    return render(request, 'quiz/quiz.html', context)


def quizDataView(request, group_id, course_id, module_id, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quiz, id=quiz_id)
    group = get_object_or_404(Group, id=group_id)
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    result = Result.objects.filter(user=user, quiz=quiz).first()
    result_attempt = 0
    if result is not None:
        result_attempt = result.attempt

    return JsonResponse(
        {
            'attempt_current': result_attempt,
            'time': quiz.time_limit_min,
            'attempts': quiz.allowed_attempts,
            'due': quiz.due_date,
        })


def add_value(dict_obj, key, value):
    ''' Adds a key-value pair to the dictionary.
        If the key already exists in the dictionary,
        it will associate multiple values with that
        key instead of overwritting its value'''
    if key not in dict_obj:
        dict_obj[key] = value
    elif isinstance(dict_obj[key], list):
        dict_obj[key].append(value)
    else:
        dict_obj[key] = [dict_obj[key], value]


def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o: (d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
    same = set(o for o in shared_keys if d1[o] == d2[o])
    return added, removed, modified, same


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required
def submitAttempt(request, group_id, course_id, module_id, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quiz, id=quiz_id)
    group = get_object_or_404(Group, id=group_id)
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)

    if request.method == 'POST':
        questions = {}
    for question in quiz.get_questions():
        answers = []
        for answer in question.get_answers():
            answers.append(answer.id)
            if answer.is_correct:
                add_value(questions, str(question.id), answer.id)

    # print('Исходный список ответов:\t', questions)
    # for k, v in zip(questions.keys(), questions.values()):
    #     print('key =', k, '\tvalues =', v)
    # print('*********************')

    # questions_POST = request.POST.getlist('question')
    answers_user = request.POST.getlist('answer')

    # разбиение ответов пользователя на ключ (id вопроса) и значения (id ответа(-ов))
    quest_user = [i.split(',', )[0] for i in answers_user]
    answ_user = [int(i.split(',', )[1]) for i in answers_user]
    # print('q=', quest_user, '\ta=', answ_user)

    questions_users = {}  # вопросы и ответы пользователя

    for quest, answ in zip(quest_user, answ_user):
        add_value(questions_users, quest, answ)

    # print('Ответы пользователя:\t', questions_users)
    # for k, v in zip(questions_users.keys(), questions_users.values()):
    #     print('key =', k, '\tvalues =', v)

    total_points = 0

    # вдруг понадобится
    # added, removed, modified, same = dict_compare(questions, questions_users)

    for k, v in zip(questions_users.keys(), questions_users.values()):
        val = questions.get(str(k), 0)
        if val != 0:
            if type(v) == list and type(val) == list:  # если пришли списки ответов, то мы их сортируем, чтобы потом сравнить
                v = sorted(v)
                val = sorted(val)

            if val == v:
                total_points += 1

    attempt = 1  # по умолч. это первая попытка

    if Result.objects.filter(user=user, quiz=quiz).exists():
        result = Result.objects.filter(user=user, quiz=quiz).first()
        attempt = result.attempt + 1

    result = Result(user=user, quiz=quiz, number_of_correct_answers=total_points, attempt=attempt)

    curr_date = datetime.date.today()  # текущая дата

    if result.attempt <= quiz.allowed_attempts and curr_date <= quiz.due_date:
        result.save()

    context = {'quiz': quiz, 'group': group, 'course': course, 'module': module,
               'result': result,
               'attempt': attempt,
               'curr_date': curr_date,
               'due_date': quiz.due_date}

    return render(request, 'quiz/quiz_result.html', context)


@login_required
def quizResults(request, group_id, course_id, module_id, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quiz, id=quiz_id)
    group = get_object_or_404(Group, id=group_id)
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    results = Result.objects.filter(user=user, quiz=quiz)
    context = {'quiz': quiz, 'group': group, 'course': course, 'module': module, 'results': results}
    return render(request, 'quiz/quiz_results.html', context)
