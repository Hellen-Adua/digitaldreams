from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:category_id>/', views.start_quiz, name='start_quiz'),
    path('mixed-quiz/', views.start_mixed_quiz, name='start_mixed_quiz'),
    path('quiz/<int:session_id>/', views.quiz_question, name='quiz_question'),
    path('submit-answer/', views.submit_answer, name='submit_answer'),
    path('results/<int:session_id>/', views.quiz_results, name='quiz_results'),
    path('revision/<int:session_id>/', views.revision_mode, name='revision_mode'),
    path('api/question-details/<int:question_id>/', views.get_question_details, name='get_question_details'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('user-stats/', views.user_stats, name='user_stats'),
]