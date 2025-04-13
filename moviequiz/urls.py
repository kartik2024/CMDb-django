from django.urls import path
from . import views

app_name = 'moviequiz'  # 👈 This is what registers the namespace

urlpatterns = [
    path('', views.home_quiz, name='home_quiz'),
    path('start/', views.start_quiz, name='start_quiz'),
    path('submit/', views.submit_quiz, name='submit_quiz'),
    path('result/', views.quiz_result, name='quiz_result'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
