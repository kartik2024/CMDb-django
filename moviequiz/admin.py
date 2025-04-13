from django.contrib import admin
from .models import QuizQuestion, UserQuizAttempt, UserScore

admin.site.register(QuizQuestion)
admin.site.register(UserQuizAttempt)
admin.site.register(UserScore)
