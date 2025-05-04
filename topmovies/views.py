from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Movie, Review, Watchlist
from .forms import LoginForm, RegisterForm, ReviewForm, AddMovieForm

def index(request):
    genres = Movie.objects.values_list('genre', flat=True).distinct()
    release_years = Movie.objects.values_list('release_year', flat=True).distinct()
    print("Session:", request.session.items())
    print("User:", request.user)
    print("Authenticated:", request.user.is_authenticated)
    return render(request, 'index.html', {'genres': genres, 'release_years': release_years})

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:  
            return redirect('/admin/') 
        return redirect('index')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful')
            if user.is_staff: 
                return redirect('/admin/')  
            return redirect('index') 

    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login')
    return render(request, 'register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')

@login_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    form = ReviewForm(request.POST or None)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.movie = movie
        review.save()
        messages.success(request, 'Your review has been added')
        return redirect('index')
    reviews = movie.reviews.all()
    return render(request, 'movie_detail.html', {'movie': movie, 'form': form, 'reviews': reviews})

@login_required
def review_view(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    form = ReviewForm(request.POST or None)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.movie = movie
        review.save()
        messages.success(request, 'Your review has been added')
        return redirect('movie_detail', movie_id=movie.id)
    return render(request, 'review.html', {'form': form, 'movie': movie})

def get_movies(request):
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 8))
    search = request.GET.get('search', '')
    genre = request.GET.get('genre', '')
    release_year = request.GET.get('release_year', '')

    movies = Movie.objects.all()
    if search:
        movies = movies.filter(title__icontains=search)
    if genre:
        movies = movies.filter(genre__icontains=genre)
    if release_year:
        movies = movies.filter(release_year=int(release_year))

   
    movies = movies[offset:offset + limit]
    data = [{'id': m.id, 'title': m.title, 'release_year': m.release_year,
             'imdb_rating': m.imdb_rating, 'poster_url': m.poster_url} for m in movies]

    return JsonResponse(data, safe=False)


@login_required
def add_movie(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('index')

    form = AddMovieForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Movie added successfully!')
        return redirect('index')
    return render(request, 'add_movie.html', {'form': form})

@login_required
def watchlist_view(request):
    movies = Movie.objects.filter(watchlist_entries__user=request.user)
    return render(request, 'watchlist.html', {'movies': movies})

@login_required
def my_ratings(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'my_ratings.html', {'reviews': reviews})

@login_required
def add_to_watchlist(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if not Watchlist.objects.filter(user=request.user, movie=movie).exists():
        Watchlist.objects.create(user=request.user, movie=movie)
        messages.success(request, 'Movie added to your watchlist.')
    else:
        messages.info(request, 'Movie is already in your watchlist.')
    return redirect('movie_detail', movie_id=movie.id)
