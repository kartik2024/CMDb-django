from django.shortcuts import render, redirect
import requests
from .models import QuizQuestion, UserQuizAttempt, QuizScore
from django.contrib.auth.decorators import login_required
import random
from django.db.models import Max, OuterRef, Subquery

FLASK_EVALUATE_URL = 'http://127.0.0.1:5001/evaluate_quiz'
FLASK_QUESTIONS_URL = 'http://127.0.0.1:5001/get_quiz_questions'


def home_quiz(request):
    return render(request, 'quiz_home.html')

@login_required
def start_quiz(request):
    if request.method == 'POST':
        answers = {
            key: value for key, value in request.POST.items() if key.startswith('question_')
        }
        formatted_answers = {key.split('_')[1]: value for key, value in answers.items()}

        try:
            response = requests.post(FLASK_EVALUATE_URL, json={'answers': formatted_answers})
            data = response.json()
        except Exception as e:
            print("Error evaluating quiz:", e)
            data = {'score': 0, 'total': 0}

        return render(request, 'quiz_result.html', data)

    try:
        response = requests.get(FLASK_QUESTIONS_URL)
        questions = response.json()
    except Exception as e:
        print("Error fetching quiz questions:", e)
        questions = []

    return render(request, 'start_quiz.html', {'questions': questions})

def submit_quiz(request):
    if request.method == 'POST':
        user_answers = {
            key.replace('question_', ''): value
            for key, value in request.POST.items()
            if key.startswith('question_')
        }

        try:
            response = requests.post(FLASK_EVALUATE_URL, json={'answers': user_answers})
            response.raise_for_status()
            score = response.json().get('score', 0)
        except Exception as e:
            print("Error calling Flask API:", e)
            score = 0

        request.session['quiz_score'] = score
        QuizScore.objects.create(user=request.user, score=score)
        return redirect('moviequiz:quiz_result')

    return redirect('moviequiz:start_quiz')

@login_required
def quiz_result(request):
    score = request.session.get('quiz_score', 0)
    total = request.session.get('total', 0)
    return render(request, 'quiz_result.html', {'score': score, 'total': total})

@login_required
def leaderboard(request):

    highest_scores = QuizScore.objects.filter(user=OuterRef('user')) \
        .order_by('-score')


    top_scores = QuizScore.objects.filter(
        id__in=QuizScore.objects.filter(
            score=Subquery(highest_scores.values('score')[:1])
        ).values('id')
    ).order_by('-score')[:10]

    return render(request, 'leaderboard.html', {'scores': top_scores})