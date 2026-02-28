from rest_framework import serializers
from .models import Movie, Seat, Booking


class MovieSerializer(serializers.ModelSerializer):
    available_seats = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'duration',
                  'poster_url', 'available_seats']


class SeatSerializer(serializers.ModelSerializer):
    movie_title = serializers.ReadOnlyField(source='movie.title')

    class Meta:
        model = Seat
        fields = ['id', 'movie', 'movie_title', 'seat_number', 'is_booked']
        read_only_fields = ['is_booked']


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    movie_title = serializers.ReadOnlyField(source='movie.title')
    seat_number = serializers.ReadOnlyField(source='seat.seat_number')

    class Meta:
        model = Booking
        fields = ['id', 'movie', 'movie_title', 'seat', 'seat_number',
                  'user', 'booking_date']
        read_only_fields = ['booking_date']

    def validate(self, data):
        seat = data.get('seat')
        movie = data.get('movie')

        # make sure the seat actually belongs to this movie
        if seat.movie != movie:
            raise serializers.ValidationError("That seat isn't for this movie.")

        if seat.is_booked:
            raise serializers.ValidationError("Seat is already taken, pick another one.")

        return data

    def create(self, validated_data):
        # attach the logged in user automatically
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
