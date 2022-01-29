from django.urls import path, include

from .views import (Home, showTeacherOffice,
                    groupDetail, courseDetail, moduleDetail,
                    showCourses, joinGroup, showModules, moduleResults,
                    sendHomework, deleteHomework,
                    )

app_name = 'classroom'

urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('teacher_office/', showTeacherOffice, name='teacher_office'),

    path('group/<int:group_id>/', groupDetail, name='group_detail'),  # не реализовано
    path('group/<int:group_id>/course/', showCourses, name='courses'),
    path('group/<int:group_id>/course/<int:course_id>/', courseDetail, name='course_detail'),  # не реализовано
    path('group/<int:group_id>/course/join/', joinGroup, name='join_group'),

    path('group/<int:group_id>/course/<int:course_id>/modules/', showModules, name='modules'),

    path('group/<int:group_id>/course/<int:course_id>/modules/<int:module_id>/homework/send/', sendHomework, name='send_homework'),
    path('group/<int:group_id>/course/<int:course_id>/modules/<int:module_id>/homework/<int:document_id>/delete/', deleteHomework, name='delete_homework'),

    path('group/<int:group_id>/course/<int:course_id>/module/<int:module_id>/', moduleDetail, name='module_detail'),
    path('group/<int:group_id>/course/<int:course_id>/module/<int:module_id>/results/', moduleResults, name='module_results'),

    path('group/<int:group_id>/course/<int:course_id>/module/<int:module_id>/quiz/<int:quiz_id>/', include('quiz.urls', namespace='quiz')),
]
