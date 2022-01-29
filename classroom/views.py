import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages

from django.views.generic import ListView, DetailView
from .models import Group, Course, Module, Content
from .forms import ContentForm
from quiz.models import Result
from quiz.models import Quiz
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect


def group_required(*group_names):
    """
    Requires user membership in at least one of the groups passed in.

    Checks is_active and allows superusers to pass regardless of group
    membership.
    """

    def in_group(u):
        return u.is_active and (u.is_superuser or bool(u.groups.filter(name__in=group_names)))

    return user_passes_test(in_group)


class Home(ListView):
    model = Group
    template_name = 'classroom/index.html'
    context_object_name = 'groups'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context


def showTeacherOffice(request):
    groups = Group.objects.all()
    courses = Course.objects.all()
    context = {'groups': groups, 'courses': courses}
    return render(request, 'classroom/teacher_office.html', context)


def groupDetail(request, group_id):
    user = request.user
    group = get_object_or_404(Group, id=group_id)
    context = {}
    return None  # потом реализую


# @group_required('Admin')
@login_required
def showCourses(request, group_id):
    user = request.user
    group = get_object_or_404(Group, id=group_id)
    courses = Course.objects.filter(group=group_id)
    users_in_group = User.objects.filter(group_joined=group)  # список студентов в группе
    # groups_for_user = Group.objects.filter(students=user) # список групп, в которые входит пользователь
    context = {}
    if user in users_in_group:
        context = {'group': group, 'courses': courses, 'students': users_in_group}
    return render(request, 'classroom/course.html', context)


def courseDetail(request, group_id, course_id):
    user = request.user
    group = get_object_or_404(Group, id=group_id)
    course = get_object_or_404(Course, id=course_id)
    context = {}
    return None  # потом реализую


# @login_required
def joinGroup(request, group_id):
    user = request.user
    if not user.is_authenticated:
        messages.error(request, 'Только зарегистрированные пользователи могут вступать в группу!')
        return redirect('classroom:index')
    else:
        # group = get_object_or_404(Group, id=group_id) # было так, заменил на ниже
        # group = Group.objects.filter(id=group_id).exists()
        if Group.objects.filter(id=group_id).exists():
            group = Group.objects.get(id=group_id)
            group.students.add(user)
            group.save()
        return redirect('classroom:courses', group_id=group_id)


@login_required
def showModules(request, group_id, course_id):
    user = request.user
    form = ContentForm()
    group = get_object_or_404(Group, id=group_id)
    course = get_object_or_404(Course, id=course_id)
    modules = Module.objects.filter(course_id=course).filter(course__group=group).filter(course__group__students=user)

    user_results = Result.objects.filter(user=user, user__group_joined=group)  # результаты тестирования пользователя
    user_files = Content.objects.filter(user=user)
    curr_date = datetime.date.today()
    context = {'user': user, 'form': form, 'group': group, 'course': course, 'modules': modules, 'user_results': user_results, 'curr_date': curr_date}
    return render(request, 'classroom/module/modules.html', context)


@login_required()
def sendHomework(request, group_id, course_id, module_id):
    user = request.user
    group = get_object_or_404(Group, id=group_id)
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    if request.method == 'POST':
        # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = ContentForm(request.POST, request.FILES)

        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            file = form.cleaned_data['file']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            module.contents.create(user=user, title=title, file=file, description=description)
            return HttpResponseRedirect(reverse('classroom:modules', kwargs={'group_id': group_id, 'course_id': course_id}))

    # Если это GET (или какой-либо ещё), создать форму по умолчанию.
    else:
        form = ContentForm()
    return render(request, 'classroom/module/modules.html', {'form': form})


@login_required()
def deleteHomework(request, group_id, course_id, module_id, document_id):
    user = request.user
    group = get_object_or_404(Group, id=group_id)
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    document = get_object_or_404(Content, id=document_id)
    if request.method == 'POST':
        document.delete()
    return showModules(request, group.id, course.id)


@login_required
def moduleDetail(request, group_id, course_id, module_id):
    user = request.user
    group = get_object_or_404(Group, id=group_id)
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    user_results = Result.objects.filter(user=user, user__group_joined=group)  # результаты тестирования пользователя
    curr_date = datetime.date.today()
    context = {'group': group, 'course': course, 'module': module, 'user_results': user_results, 'curr_date': curr_date}
    return render(request, 'classroom/module/module_detail.html', context)


@group_required('Admin')
@login_required
def moduleResults(request, group_id, course_id, module_id):
    user = request.user
    group = get_object_or_404(Group, id=group_id)
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    # # user_results = Result.objects.filter(user__course_created__modules=module)  # результаты тестирования пользователя
    # # user_results = User.objects.filter(result_received__quiz__module=module)
    # # print(Result.objects.filter(user__in=user_results, quiz__module__course=course, quiz__module=module))
    # # print(user_results)
    #
    # user_module = User.objects.filter(result_received__quiz__module=module)  # пользователи, проходившие опрос по данному модулю
    # user_results = Result.objects.filter(user__in=user_module, quiz__module_id=module.id)

    user_results = Result.objects.filter(quiz__module_id=module.id)  # результаты тестирования пользователей по данному модулю
    users_in_group = User.objects.filter(group_joined=group)  # список студентов в группе

    context = {'group': group, 'course': course, 'module': module, 'user_results': user_results, 'users_in_group': users_in_group}
    return render(request, 'classroom/module/module_results.html', context)
