from django.shortcuts import render, redirect
from .models import QuizQuestion, UserQuizAttempt, QuizScore
from django.contrib.auth.decorators import login_required
import random
from django.db.models import Max, OuterRef, Subquery


def home_quiz(request):
    return render(request, 'quiz_home.html')


QUIZ_QUESTIONS = [
    {
        'id': 1,
        'question': "What does Andy Dufresne carve on the wall of his prison cell in *The Shawshank Redemption*?",
        'options': ['A chessboard', 'A Bible verse', 'A tunnel', 'A poster of Rita Hayworth'],
        'answer': 'A tunnel'
    },
    {
        'id': 2,
        'question': "In *Interstellar*, what is the name of the planet covered in shallow water and time dilation?",
        'options': ['Miller’s Planet', 'Edmunds’ Planet', 'Mann’s Planet', 'Murph’s Planet'],
        'answer': 'Miller’s Planet'
    },
    {
        'id': 3,
        'question': "In *Oppenheimer*, which equation plays a key symbolic role in the development of the bomb?",
        'options': ['E=mc^2', 'Schrödinger’s Equation', 'Heisenberg’s Uncertainty Principle', 'The Manhattan Equation'],
        'answer': 'E=mc^2'
    },
    {
        'id': 4,
        'question': "Which film has the quote: “I’m gonna make him an offer he can’t refuse”?",
        'options': ['Scarface', 'The Godfather', 'Goodfellas', 'Casino'],
        'answer': 'The Godfather'
    },
    {
        'id': 5,
        'question': "In *The Dark Knight*, who played Harvey Dent / Two-Face?",
        'options': ['Aaron Eckhart', 'Cillian Murphy', 'Tom Hardy', 'Joseph Gordon-Levitt'],
        'answer': 'Aaron Eckhart'
    },
    {
        'id': 6,
        'question': "Which movie ends with the line: “After all, tomorrow is another day”?",
        'options': ['Gone with the Wind', 'Casablanca', 'Citizen Kane', 'The Sound of Music'],
        'answer': 'Gone with the Wind'
    },
    {
        'id': 7,
        'question': "In *Fight Club*, what is the first rule of Fight Club?",
        'options': ['Don’t talk about Fight Club', 'No shirts', 'First rule is obey the second rule', 'No shoes allowed'],
        'answer': 'Don’t talk about Fight Club'
    },
    {
        'id': 8,
        'question': "In *Inception*, what object does Cobb use to check if he’s dreaming?",
        'options': ['A ring', 'A spinning top', 'A photo', 'A coin'],
        'answer': 'A spinning top'
    },
    {
        'id': 9,
        'question': "In *Forrest Gump*, what company does Forrest invest in?",
        'options': ['Apple', 'IBM', 'Microsoft', 'Nike'],
        'answer': 'Apple'
    },
    {
        'id': 10,
        'question': "Which character says “Why so serious?” in *The Dark Knight*?",
        'options': ['Batman', 'Alfred', 'Harvey Dent', 'The Joker'],
        'answer': 'The Joker'
    },
]

@login_required
def start_quiz(request):
    if request.method == 'POST':
        score = 0
        for q in QUIZ_QUESTIONS:
            selected = request.POST.get(str(q['id']))
            if selected == q['answer']:
                score += 1
        return render(request, 'quiz_result.html', {
            'score': score,
            'total': len(QUIZ_QUESTIONS)
        })
    
    return render(request, 'start_quiz.html', {'questions': QUIZ_QUESTIONS})

def submit_quiz(request):
    if request.method == 'POST':
        score = 0
        print(request.POST['question_1'])

        for question in QUIZ_QUESTIONS:
            qid = str(question['id'])
            selected_answer = request.POST[f'question_{qid}']
            correct_answer = question['answer']

            # Debugging output to make sure everything matches
            print(f"Q{qid} -> Selected: '{selected_answer}' | Correct: '{correct_answer}'")

            if selected_answer and selected_answer.strip() == correct_answer.strip():
                score += 1
            else:
                print(f"Incorrect or no match for Q{qid}")
        
        

        print(f"Final Score: {score}")
        request.session['quiz_score'] = score

        QuizScore.objects.create(user=request.user, score=score)

        return redirect('moviequiz:quiz_result')

    return redirect('moviequiz:start_quiz')

@login_required
def quiz_result(request):
    score = request.session.get('quiz_score', 0)
    total = len(QUIZ_QUESTIONS)
    return render(request, 'quiz_result.html', {'score': score, 'total': total})


@login_required
def leaderboard(request):
    # Subquery to get the highest score per user
    highest_scores = QuizScore.objects.filter(user=OuterRef('user')) \
        .order_by('-score')

    # Filter only the top score per user
    top_scores = QuizScore.objects.filter(
        id__in=QuizScore.objects.filter(
            score=Subquery(highest_scores.values('score')[:1])
        ).values('id')
    ).order_by('-score')[:10]

    return render(request, 'leaderboard.html', {'scores': top_scores})