from django.urls import path

from .views import quizView, quizDataView, quizResults, submitAttempt

app_name = 'quiz'

urlpatterns = [
    path('', quizView, name='quiz'),
    path('data/', quizDataView, name='quiz_Data_View'),
    path('results', quizResults, name='quiz_results'),
    path('submit/', submitAttempt, name='submit_quiz'),

]
