from django import template
from quiz.models import Result
from classroom.models import Content
from django.db.models import Max

register = template.Library()


@register.filter
def get_results_by_user(self):
    return Result.objects.filter(user=self.user, quiz=self.quiz)


# фильтр для вывода документов пользователя для заданного модуля
@register.filter
def get_user_content(user, module):
    return Content.objects.filter(user=user, module=module)


# фильтр для получения лучшего результата тестирования пользователя для заданного модуля
@register.filter
def get_user_results(user, module):
    results = Result.objects.filter(user=user, quiz__module=module).values('user', 'quiz__title').annotate(Max('number_of_correct_answers'))
    return results
