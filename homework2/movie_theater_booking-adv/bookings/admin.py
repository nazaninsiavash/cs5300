from django.contrib import admin
from .models import Movie, Seat, Booking


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_date', 'duration', 'available_seats']
    search_fields = ['title']
    list_filter = ['release_date']


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['seat_number', 'movie', 'is_booked']
    list_filter = ['is_booked', 'movie']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'seat', 'booking_date']
    list_filter = ['movie']
