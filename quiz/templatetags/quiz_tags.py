from django import template
from classroom.models import Group

register = template.Library()


@register.filter(name='words_ending')
def question_ending(value, arg="вопрос,вопроса,вопросов"):
    args = arg.split(",")
    number = abs(int(value))
    a = number % 10
    b = number % 100

    if (a == 1) and (b != 11):
        return args[0]
    elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
        return args[1]
    else:
        return args[2]



