import json
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CMDb.settings')
django.setup()

from topmovies.models import Movie

def import_json_to_django():
    # Delete all existing movies
    Movie.objects.all().delete()
    print("✅ Cleared existing movies.")

    # Load movies from JSON
    with open('movies_data.json', 'r') as json_file:
        movies = json.load(json_file)

    for movie in movies:
        try:
            release_year = movie.get('imdb_rating', None)

            if isinstance(release_year, str):
                try:
                    release_year = int(release_year[:4])
                except ValueError:
                    print(f"⚠️ Invalid release_year for {movie['title']}: {release_year}")
                    release_year = None

            if release_year is None:
                print(f"⏭️ Skipping movie due to invalid release_year: {movie['title']}")
                continue

            Movie.objects.create(
                title=movie['title'],
                release_year=release_year,
                imdb_rating=float(movie['imdb_rating']) if isinstance(movie['imdb_rating'], (int, float)) else None,
                poster_url=movie['poster_url'],
                genre=movie['genre'],
                release_date=movie['release_date'],
                description=movie['description']
            )
            print(f"✅ Added: {movie['title']}")
        except KeyError as e:
            print(f"❌ Missing key {e} in movie: {movie}")
        except ValueError as e:
            print(f"❌ Invalid format in {movie['title']}: {e}")
        except Exception as e:
            print(f"❌ Error inserting {movie['title']}: {e}")

if __name__ == "__main__":
    import_json_to_django()
