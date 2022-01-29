from django.contrib import admin

from .models import Group, Course, Module, Content


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'description')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('get_group', 'title', 'description', 'owner')
    list_filter = ('group',)
    list_display_links = ('get_group', 'title')
    search_fields = ['title', ]
    search_help_text = 'Поиск по названию'

    @admin.display(description='Группа', ordering='course__group')
    def get_group(self, obj):
        return obj.group.title


class ContentInline(admin.StackedInline):
    model = Content
    extra = 1


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('get_group', 'course', 'title', 'hours')
    list_filter = ('course__group', 'course')
    list_display_links = ('get_group', 'course')
    search_fields = ['description']
    search_help_text = 'Поиск по названию'
    inlines = [ContentInline]

    @admin.display(description='Группа', ordering='module__course__group')
    def get_group(self, obj):
        return obj.course.group.title
