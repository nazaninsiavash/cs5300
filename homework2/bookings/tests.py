"""
tests for the booking app
covers models, api endpoints, and the main UI views
"""

import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date

from .models import Movie, Seat, Booking


# quick helpers so i dont repeat this setup everywhere

def make_movie(**kwargs):
    defaults = {
        'title': 'Test Movie',
        'description': 'just a test movie',
        'release_date': date(2024, 6, 15),
        'duration': 120,
    }
    defaults.update(kwargs)
    return Movie.objects.create(**defaults)


def make_seat(movie, number='A1', booked=False):
    return Seat.objects.create(movie=movie, seat_number=number, is_booked=booked)


# --- model tests ---

class MovieModelTest(TestCase):

    def test_movie_creation(self):
        movie = make_movie()
        self.assertEqual(movie.title, 'Test Movie')
        self.assertEqual(movie.duration, 120)
        # make sure the fields are the right types
        self.assertIsInstance(movie.title, str)
        self.assertIsInstance(movie.duration, int)

    def test_movie_str(self):
        movie = make_movie(title='Interstellar')
        self.assertEqual(str(movie), 'Interstellar')

    def test_available_seats_counts_only_free(self):
        movie = make_movie()
        make_seat(movie, 'A1', booked=False)
        make_seat(movie, 'A2', booked=True)
        make_seat(movie, 'A3', booked=False)
        self.assertEqual(movie.available_seats, 2)

    def test_available_seats_zero_when_all_booked(self):
        movie = make_movie()
        make_seat(movie, 'A1', booked=True)
        self.assertEqual(movie.available_seats, 0)

    def test_available_seats_all_free(self):
        movie = make_movie()
        make_seat(movie, 'A1')
        make_seat(movie, 'A2')
        self.assertEqual(movie.available_seats, 2)


class SeatModelTest(TestCase):

    def setUp(self):
        self.movie = make_movie()

    def test_seat_defaults_to_available(self):
        seat = make_seat(self.movie, 'B5')
        self.assertFalse(seat.is_booked)
        self.assertEqual(seat.seat_number, 'B5')
        self.assertIsInstance(seat.seat_number, str)

    def test_seat_str_available(self):
        seat = make_seat(self.movie, 'C3')
        self.assertIn('C3', str(seat))
        self.assertIn('Available', str(seat))

    def test_seat_str_booked(self):
        seat = make_seat(self.movie, 'C4', booked=True)
        self.assertIn('C4', str(seat))
        self.assertIn('Booked', str(seat))

    def test_cant_have_duplicate_seat_numbers(self):
        from django.db import IntegrityError
        make_seat(self.movie, 'A1')
        with self.assertRaises(IntegrityError):
            make_seat(self.movie, 'A1')


class BookingModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('testuser', password='pass123')
        self.movie = make_movie()
        self.seat = make_seat(self.movie, 'D4')

    def test_booking_marks_seat_as_booked(self):
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_booked)

    def test_booking_str_has_expected_content(self):
        booking = Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        result = str(booking)
        self.assertIn('testuser', result)
        self.assertIn('Test Movie', result)
        self.assertIn('D4', result)

    def test_deleting_booking_frees_seat(self):
        booking = Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        booking.delete()
        self.seat.refresh_from_db()
        self.assertFalse(self.seat.is_booked)

    def test_booking_date_is_set_automatically(self):
        booking = Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        self.assertIsNotNone(booking.booking_date)

    def test_booking_links_correct_user(self):
        booking = Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        self.assertEqual(booking.user.username, 'testuser')
        self.assertIsInstance(booking.user, User)


# --- api tests ---

class MovieAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('apiuser', password='pass123')
        self.movie = make_movie(title='API Movie')

    def test_anyone_can_list_movies(self):
        response = self.client.get('/api/movies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        # check actual content, not just length
        self.assertEqual(response.data['results'][0]['title'], 'API Movie')
        self.assertEqual(response.data['results'][0]['duration'], 120)

    def test_get_single_movie(self):
        response = self.client.get(f'/api/movies/{self.movie.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'API Movie')
        self.assertEqual(response.data['duration'], 120)
        self.assertIn('available_seats', response.data)

    def test_cant_create_movie_without_login(self):
        data = {
            'title': 'New',
            'description': 'Desc',
            'release_date': '2024-01-01',
            'duration': 90,
        }
        response = self.client.post('/api/movies/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_movie_when_logged_in(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Film',
            'description': 'some film',
            'release_date': '2024-03-01',
            'duration': 105,
        }
        response = self.client.post('/api/movies/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 2)
        # check the returned data matches what we sent
        self.assertEqual(response.data['title'], 'New Film')
        self.assertEqual(response.data['duration'], 105)

    def test_update_title(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'/api/movies/{self.movie.id}/', {'title': 'Renamed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, 'Renamed')

    def test_update_duration(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'/api/movies/{self.movie.id}/', {'duration': 200})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.duration, 200)

    def test_update_description(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f'/api/movies/{self.movie.id}/', {'description': 'updated desc'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.description, 'updated desc')

    def test_delete_movie(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/movies/{self.movie.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movie.objects.count(), 0)

    def test_seats_action_returns_correct_seats(self):
        make_seat(self.movie, 'A1')
        make_seat(self.movie, 'A2')
        response = self.client.get(f'/api/movies/{self.movie.id}/seats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        seat_numbers = [s['seat_number'] for s in response.data]
        self.assertIn('A1', seat_numbers)
        self.assertIn('A2', seat_numbers)

    def test_search_by_exact_title(self):
        make_movie(title='Unique Title XYZ')
        response = self.client.get('/api/movies/?search=Unique')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Unique Title XYZ')

    def test_search_no_match_returns_empty(self):
        response = self.client.get('/api/movies/?search=nonexistent')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_search_case_insensitive(self):
        # 'api' (lowercase) should still match 'API Movie'
        response = self.client.get('/api/movies/?search=api')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class SeatAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.movie = make_movie()
        self.seat = make_seat(self.movie, 'E1')

    def test_list_seats(self):
        response = self.client.get('/api/seats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['seat_number'], 'E1')

    def test_filter_seats_by_movie(self):
        other_movie = make_movie(title='Other')
        make_seat(other_movie, 'F1')
        response = self.client.get(f'/api/seats/?movie={self.movie.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for s in response.data['results']:
            self.assertEqual(s['movie'], self.movie.id)

    def test_available_endpoint_only_returns_free_seats(self):
        make_seat(self.movie, 'E2', booked=True)
        response = self.client.get(f'/api/seats/available/?movie={self.movie.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # should only get E1 back, not E2
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['seat_number'], 'E1')
        for s in response.data:
            self.assertFalse(s['is_booked'])

    def test_available_seat_is_booked_false(self):
        seat = make_seat(self.movie, 'A1', booked=False)
        response = self.client.get(f'/api/seats/{seat.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_booked'])
        self.assertEqual(response.data['seat_number'], 'A1')

    def test_booked_seat_is_booked_true(self):
        seat = make_seat(self.movie, 'B2', booked=True)
        response = self.client.get(f'/api/seats/{seat.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_booked'])
        self.assertEqual(response.data['seat_number'], 'B2')


class BookingAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('booker', password='pass123')
        self.other_user = User.objects.create_user('other', password='pass123')
        self.movie = make_movie()
        self.seat = make_seat(self.movie, 'G1')

    def test_need_to_be_logged_in_for_get(self):
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_need_to_be_logged_in_for_post(self):
        response = self.client.post('/api/bookings/', {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_need_to_be_logged_in_for_delete(self):
        response = self.client.delete('/api/bookings/999/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_booking(self):
        self.client.force_authenticate(user=self.user)
        data = {'movie': self.movie.id, 'seat': self.seat.id}
        response = self.client.post('/api/bookings/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # check actual content
        self.assertEqual(response.data['user'], 'booker')
        self.assertEqual(response.data['movie_title'], 'Test Movie')
        self.assertEqual(response.data['seat_number'], 'G1')

    def test_cant_book_same_seat_twice(self):
        self.client.force_authenticate(user=self.user)
        data = {'movie': self.movie.id, 'seat': self.seat.id}
        self.client.post('/api/bookings/', data)
        response = self.client.post('/api/bookings/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_seat_must_belong_to_movie(self):
        self.client.force_authenticate(user=self.user)
        other_movie = make_movie(title='Wrong Movie')
        data = {'movie': other_movie.id, 'seat': self.seat.id}
        response = self.client.post('/api/bookings/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_see_other_users_bookings(self):
        seat2 = make_seat(self.movie, 'G2')
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        Booking.objects.create(movie=self.movie, seat=seat2, user=self.other_user)

        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        # make sure it's our booking, not the other user's
        self.assertEqual(response.data['results'][0]['user'], 'booker')

    def test_cancel_booking(self):
        self.client.force_authenticate(user=self.user)
        booking = Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        response = self.client.delete(f'/api/bookings/{booking.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 0)
        self.seat.refresh_from_db()
        self.assertFalse(self.seat.is_booked)


# --- UI view tests ---

class UIViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('uiuser', password='pass123')
        self.movie = make_movie(title='UI Movie')
        self.seat = make_seat(self.movie, 'H1')

    def test_movie_list_loads(self):
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'UI Movie')
        # check movies are actually passed to template
        self.assertIn('movies', response.context)
        self.assertEqual(response.context['movies'].count(), 1)

    def test_movie_list_is_public(self):
        # no login needed
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)

    def test_seat_booking_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('book_seat', args=[self.movie.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_history_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('booking_history'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_seat_booking_page_loads_when_logged_in(self):
        self.client.login(username='uiuser', password='pass123')
        response = self.client.get(reverse('book_seat', args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'UI Movie')
        # verify template has the seat and movie context we expect
        self.assertIn('movie', response.context)
        self.assertIn('seats', response.context)
        self.assertEqual(response.context['movie'].title, 'UI Movie')

    def test_booking_via_post_redirects_to_history(self):
        self.client.login(username='uiuser', password='pass123')
        response = self.client.post(
            reverse('book_seat', args=[self.movie.id]),
            {'seat_id': self.seat.id},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('booking_history'))
        self.assertEqual(Booking.objects.count(), 1)
        # check the booking actually has the right seat
        booking = Booking.objects.first()
        self.assertEqual(booking.seat.seat_number, 'H1')
        self.assertEqual(booking.user.username, 'uiuser')

    def test_booking_already_booked_seat_shows_error(self):
        self.seat.is_booked = True
        self.seat.save()
        self.client.login(username='uiuser', password='pass123')
        response = self.client.post(
            reverse('book_seat', args=[self.movie.id]),
            {'seat_id': self.seat.id},
        )
        self.assertEqual(response.status_code, 200)
        msgs = list(response.context['messages'])
        self.assertTrue(any('already booked' in str(m) for m in msgs))
        # no new booking should have been created
        self.assertEqual(Booking.objects.count(), 0)

    def test_history_shows_user_bookings(self):
        self.client.login(username='uiuser', password='pass123')
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        response = self.client.get(reverse('booking_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'UI Movie')
        # verify the booking appears in context
        self.assertEqual(response.context['bookings'].count(), 1)
        self.assertEqual(response.context['bookings'][0].seat.seat_number, 'H1')

    def test_cancel_booking_removes_it(self):
        self.client.login(username='uiuser', password='pass123')
        booking = Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        response = self.client.post(reverse('cancel_booking', args=[booking.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.count(), 0)
        self.seat.refresh_from_db()
        self.assertFalse(self.seat.is_booked)

    def test_cant_cancel_someone_elses_booking(self):
        other = User.objects.create_user('other2', password='pass123')
        booking = Booking.objects.create(movie=self.movie, seat=self.seat, user=other)
        self.client.login(username='uiuser', password='pass123')
        response = self.client.post(reverse('cancel_booking', args=[booking.id]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Booking.objects.count(), 1)


# --- parametrized tests (pytest-django) ---
# these run with: pytest --ds=movie_theater_booking.settings

@pytest.mark.django_db
@pytest.mark.parametrize('title,duration', [
    ('Inception', 148),
    ('Parasite', 132),
    ('The Dark Knight', 152),
])
def test_movie_fields_are_correct_types(title, duration):
    # check that movie fields store and return what we put in
    movie = Movie.objects.create(
        title=title,
        description='test',
        release_date=date(2024, 1, 1),
        duration=duration,
    )
    assert movie.title == title
    assert movie.duration == duration
    assert isinstance(movie.title, str)
    assert isinstance(movie.duration, int)


@pytest.mark.django_db
@pytest.mark.parametrize('seat_num', ['A1', 'B3', 'C10', 'Z99'])
def test_various_seat_number_formats(seat_num):
    movie = Movie.objects.create(
        title='test',
        description='x',
        release_date=date(2024, 1, 1),
        duration=100,
    )
    seat = Seat.objects.create(movie=movie, seat_number=seat_num)
    assert seat.seat_number == seat_num
    assert not seat.is_booked
    assert isinstance(seat.seat_number, str)


@pytest.mark.django_db
@pytest.mark.parametrize('search_term,expected_count', [
    ('Inception', 1),
    ('nonexistent', 0),
    ('inc', 1),  # partial match
])
def test_movie_search_api(client, search_term, expected_count):
    Movie.objects.create(
        title='Inception',
        description='dreams',
        release_date=date(2024, 1, 1),
        duration=148,
    )
    response = client.get(f'/api/movies/?search={search_term}')
    assert response.status_code == 200
    assert len(response.json()['results']) == expected_count


@pytest.mark.django_db
@pytest.mark.parametrize('field,new_value', [
    ('title', 'Renamed Movie'),
    ('duration', 999),
    ('description', 'totally new description'),
])
def test_partial_movie_update(field, new_value):
    # test that each field can be patched independently
    from rest_framework.test import APIClient as DRFClient
    user = User.objects.create_user('patchuser', password='pass')
    movie = Movie.objects.create(
        title='Original',
        description='original desc',
        release_date=date(2024, 1, 1),
        duration=100,
    )
    api = DRFClient()
    api.force_authenticate(user=user)
    resp = api.patch(f'/api/movies/{movie.id}/', {field: new_value})
    assert resp.status_code == 200
    movie.refresh_from_db()
    assert getattr(movie, field) == new_value


@pytest.mark.django_db
@pytest.mark.parametrize('seat_num,booked', [
    ('A1', False),
    ('B2', True),
    ('C3', False),
])
def test_seat_booked_status_via_api(seat_num, booked):
    from rest_framework.test import APIClient as DRFClient
    movie = Movie.objects.create(
        title='test',
        description='x',
        release_date=date(2024, 1, 1),
        duration=100,
    )
    seat = Seat.objects.create(movie=movie, seat_number=seat_num, is_booked=booked)
    api = DRFClient()
    resp = api.get(f'/api/seats/{seat.id}/')
    assert resp.status_code == 200
    assert resp.json()['is_booked'] == booked
    assert resp.json()['seat_number'] == seat_num
