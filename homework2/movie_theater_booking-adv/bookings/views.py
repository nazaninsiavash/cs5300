from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer


# --- API viewsets ---

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['release_date', 'title', 'duration']

    @action(detail=True, methods=['get'], url_path='seats')
    def seats(self, request, pk=None):
        movie = self.get_object()
        seats = movie.seat_set.all()
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['seat_number', 'is_booked']

    def get_queryset(self):
        queryset = Seat.objects.all()
        # filter by movie if ?movie=id is passed
        movie_id = self.request.query_params.get('movie', None)
        if movie_id:
            queryset = queryset.filter(movie_id=movie_id)
        return queryset

    @action(detail=False, methods=['get'])
    def available(self, request):
        available_seats = Seat.objects.filter(is_booked=False)
        movie_id = request.query_params.get('movie', None)
        if movie_id:
            available_seats = available_seats.filter(movie_id=movie_id)
        serializer = self.get_serializer(available_seats, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # users should only see their own bookings
        return Booking.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.delete()
        return Response({"message": "Booking cancelled."}, status=status.HTTP_204_NO_CONTENT)


# --- template views ---

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {'movies': movies})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/history/')
    else:
        form = UserCreationForm()
    return render(request, 'bookings/signup.html', {'form': form})


@login_required
def seat_booking(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    seats = Seat.objects.filter(movie=movie).order_by('seat_number')

    if request.method == 'POST':
        seat_id = request.POST.get('seat_id')
        seat = get_object_or_404(Seat, pk=seat_id, movie=movie)

        if seat.is_booked:
            messages.error(request, 'That seat is already booked, try another one.')
        else:
            Booking.objects.create(movie=movie, seat=seat, user=request.user)
            messages.success(request, f'Booked seat {seat.seat_number} for {movie.title}!')
            return HttpResponseRedirect('/history/')

    return render(request, 'bookings/seat_booking.html', {'movie': movie, 'seats': seats})


@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).select_related('movie', 'seat')
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    if request.method == 'POST':
        movie_title = booking.movie.title
        seat_number = booking.seat.seat_number
        booking.delete()
        messages.success(request, f'Cancelled booking for seat {seat_number} - {movie_title}.')
    return HttpResponseRedirect('/history/')