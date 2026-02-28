"""
seeds the db with some sample movies and seats so theres something to look at
run with: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bookings.models import Movie, Seat
from datetime import date


SAMPLE_MOVIES = [
    {
        'title': 'The Housemaid',
        'description': (
            'A young woman takes a job as a housemaid for a wealthy family, '
            'but soon discovers dark secrets hidden behind their perfect facade.'
        ),
        'release_date': date(2025, 2, 19),
        'duration': 112,
        'poster_url': 'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcRFQkWrP62a03eDmpaDIJsxra5_KAPk1QABqs3YFx8tt191uLBd',
    },
    {
        'title': 'Drop',
        'description': (
            'Violet is a widowed mother who goes to an upscale restaurant to meet Henry, her charming and handsome date. However, her pleasant evening soon turns into a living nightmare when she receives phone messages from a mysterious, hooded figure who threatens to kill her young son and sister unless she kills Henry.'
        ),
        'release_date': date(2025, 3, 9),
        'duration': 94,
        'poster_url': 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRD5gRf2gOD2JmSvHkv1VN0rBFSd0Ud5pLvFpzOigKjtnlG8klZ',
    },
    {
        'title': 'It Ends with Us',
        'description': (
            'A young woman navigates a complicated romance while confronting '
            'difficult truths about love, strength, and what it means to start over.'
        ),
        'release_date': date(2024, 8, 9),
        'duration': 130,
        'poster_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQ_LJYfL1EsiycSNulq19guoxSCMr6PTAXLaCMKY3xAjL56pZ3',
    },
    {
        'title': 'Mamma Mia!',
        'description': (
            'The story of a bride trying to find her father and invite him '
            'to her wedding, told through the songs of ABBA.'
        ),
        'release_date': date(2008, 7, 18),
        'duration': 108,
        'poster_url': 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcSwRx28MVLxKdKjjH46EbbDKx6q6N3nJMt-tTsy5kr6Ybnq7wEG',
    },
]

SEAT_ROWS = ['A', 'B', 'C', 'D', 'E']
SEATS_PER_ROW = 8


class Command(BaseCommand):
    help = 'adds sample movies and a demo user to the db'

    def handle(self, *args, **options):
        self.stdout.write('seeding...')

        if not User.objects.filter(username='demo').exists():
            User.objects.create_user('demo', password='demo1234')
            self.stdout.write(self.style.SUCCESS('  created demo user (demo / demo1234)'))

        for movie_data in SAMPLE_MOVIES:
            movie, created = Movie.objects.get_or_create(
                title=movie_data['title'],
                defaults=movie_data
            )
            if created:
                for row in SEAT_ROWS:
                    for col in range(1, SEATS_PER_ROW + 1):
                        Seat.objects.create(movie=movie, seat_number=f"{row}{col}")
                self.stdout.write(self.style.SUCCESS(f'  added: {movie.title}'))
            else:
                self.stdout.write(f'  skipped (already exists): {movie.title}')

        self.stdout.write(self.style.SUCCESS('done! login with demo / demo1234'))