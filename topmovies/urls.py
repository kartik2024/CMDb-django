from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/review/', views.review_view, name='review_view'),
    path('api/movies/', views.get_movies, name='get_movies'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('watchlist/', views.watchlist_view, name='watchlist'),
    path('my_ratings/', views.my_ratings, name='my_ratings'),
    path('add_to_watchlist/<int:movie_id>/', views.add_to_watchlist, name='add_to_watchlist'),
]
