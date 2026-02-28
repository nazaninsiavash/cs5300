from django.db import models
from django.contrib.auth.models import User


# movie model - stores all the info about each film
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.PositiveIntegerField()  # in minutes
    poster_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['-release_date']

    def __str__(self):
        return self.title

    @property
    def available_seats(self):
        # just counts seats that havent been booked yet
        return self.seat_set.filter(is_booked=False).count()


class Seat(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)  # like A1, B5 etc
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('movie', 'seat_number')
        ordering = ['seat_number']

    def __str__(self):
        status = "Booked" if self.is_booked else "Available"
        return f"Seat {self.seat_number} - {self.movie.title} ({status})"


class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-booking_date']

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} (Seat {self.seat.seat_number})"

    def save(self, *args, **kwargs):
        # mark the seat as taken when booking is saved
        self.seat.is_booked = True
        self.seat.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # free up seat if someone cancels
        self.seat.is_booked = False
        self.seat.save()
        super().delete(*args, **kwargs)
