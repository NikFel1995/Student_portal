from django.contrib import admin

from .models import Quiz, Question, Answer, Result


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'time_limit_min', 'allowed_attempts', 'due_date')
    # list_display_links = ('title',)
    list_editable = ('time_limit_min', 'allowed_attempts', 'due_date')
    list_filter = ('module__course__group', 'time_limit_min', 'due_date')
    search_fields = ['title', ]
    fieldsets = (
        (None, {
            'fields': ('module', 'title', 'description',)
        }),
        ('Дополнительно', {
            'classes': ('collapse',),
            'fields': ('time_limit_min', 'allowed_attempts', 'due_date'),
        }),
    )


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3
    can_delete = True


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('title', 'quiz',)
    list_filter = ('quiz',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'title', 'is_correct',)
    list_editable = ('is_correct',)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_group', 'get_course', 'get_module', 'quiz', 'number_of_correct_answers', 'attempt', 'completed')
    list_display_links = ('user', 'get_group', 'get_course', 'get_module',)
    list_filter = ('quiz__module__course__group', 'quiz__module__course', 'completed')
    search_fields = ['quiz', 'user']

    @admin.display(description='Модуль', ordering='result__quiz__module')
    def get_module(self, obj):
        return obj.quiz.module.title

    @admin.display(description='Курс', ordering='result__quiz__module__course')
    def get_course(self, obj):
        return obj.quiz.module.course.title

    @admin.display(description='Группа', ordering='result__quiz__module__course__group')
    def get_group(self, obj):
        return obj.quiz.module.course.group.title
