from django import template
from classroom.models import Group

register = template.Library()


@register.filter()
def user_group(user):
    if not user.is_anonymous:
        groups_for_user = Group.objects.filter(students=user).first()  # список групп, в которые входит пользователь. Берем первую группу
        if groups_for_user is None:
            return None
        return groups_for_user.id
    return None


@register.filter('has_group')
def has_group(user, groups_name):
    return user.is_active and user.is_superuser or bool(user.groups.filter(name__in=groups_name))
