"""
Behave step definitions for the Movie Theater Booking BDD tests.
Run with: behave bookings/features/
"""

import os

import django
from behave import given, when, then

# django setup needs to happen before importing models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_theater_booking.settings')
django.setup()

from django.test import Client  # noqa: E402
from django.contrib.auth.models import User  # noqa: E402
from bookings.models import Movie, Seat, Booking  # noqa: E402
from datetime import date  # noqa: E402


@given('the database is clean')
def step_clean_db(context):
    Booking.objects.all().delete()
    Seat.objects.all().delete()
    Movie.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    context.client = Client()


@given('a user "{username}" with password "{password}" exists')
def step_create_user(context, username, password):
    context.user = User.objects.create_user(username=username, password=password)


@given('a movie "{title}" with {n} available seats exists')
def step_create_movie(context, title, n):
    movie = Movie.objects.create(
        title=title,
        description='A thrilling movie.',
        release_date=date(2024, 1, 1),
        duration=148,
    )
    for i in range(int(n)):
        row = chr(65 + i // 5)   # A, B, C...
        col = (i % 5) + 1
        Seat.objects.create(movie=movie, seat_number=f"{row}{col}")
    context.movie = movie


@given('I am logged in as "{username}" with password "{password}"')
def step_login(context, username, password):
    context.client.login(username=username, password=password)


@when('I visit the movie list page')
def step_visit_movie_list(context):
    context.response = context.client.get('/')


@then('I should see "{text}" in the response')
def step_see_text(context, text):
    assert text.encode() in context.response.content, \
        f'"{text}" not found in response. Content: {context.response.content[:500]}'


@when('I book seat "{seat_num}" for movie "{title}"')
def step_book_seat(context, seat_num, title):
    movie = Movie.objects.get(title=title)
    seat = Seat.objects.get(movie=movie, seat_number=seat_num)
    from django.urls import reverse
    context.response = context.client.post(
        reverse('book_seat', args=[movie.id]),
        {'seat_id': seat.id}
    )
    context.seat = seat
    context.movie = movie


@then('the booking should be created successfully')
def step_booking_created(context):
    assert Booking.objects.count() == 1, f"Expected 1 booking, got {Booking.objects.count()}"


@then('seat "{seat_num}" should be marked as booked')
def step_seat_is_booked(context, seat_num):
    seat = Seat.objects.get(seat_number=seat_num, movie=context.movie)
    assert seat.is_booked, f"Seat {seat_num} is not marked as booked"


@given('seat "{seat_num}" for movie "{title}" is already booked')
def step_seat_already_booked(context, seat_num, title):
    movie = Movie.objects.get(title=title)
    seat = Seat.objects.get(movie=movie, seat_number=seat_num)
    seat.is_booked = True
    seat.save()


@when('I try to book seat "{seat_num}" for movie "{title}"')
def step_try_book_seat(context, seat_num, title):
    movie = Movie.objects.get(title=title)
    seat = Seat.objects.get(movie=movie, seat_number=seat_num)
    from django.urls import reverse
    context.response = context.client.post(
        reverse('book_seat', args=[movie.id]),
        {'seat_id': seat.id}
    )
    context.seat = seat
    context.movie = movie


@then('I should see an error about the seat being already booked')
def step_see_error(context):
    from django.contrib.messages import get_messages
    msgs = [str(m) for m in get_messages(context.response.wsgi_request)]
    assert any('already booked' in m for m in msgs), \
        f"Expected 'already booked' message but got: {msgs}"


@given('I have a booking for seat "{seat_num}" in movie "{title}"')
def step_create_booking(context, seat_num, title):
    movie = Movie.objects.get(title=title)
    seat = Seat.objects.get(movie=movie, seat_number=seat_num)
    context.booking = Booking.objects.create(
        movie=movie, seat=seat, user=context.user
    )
    context.movie = movie
    context.seat = seat


@when('I visit the booking history page')
def step_visit_history(context):
    from django.urls import reverse
    context.response = context.client.get(reverse('booking_history'))


@when('I cancel my booking')
def step_cancel_booking(context):
    from django.urls import reverse
    context.response = context.client.post(
        reverse('cancel_booking', args=[context.booking.id])
    )


@then('the booking should be removed')
def step_booking_removed(context):
    assert Booking.objects.count() == 0, "Booking was not removed"


@then('seat "{seat_num}" should be available again')
def step_seat_available(context, seat_num):
    seat = Seat.objects.get(seat_number=seat_num, movie=context.movie)
    assert not seat.is_booked, f"Seat {seat_num} is still marked as booked"
