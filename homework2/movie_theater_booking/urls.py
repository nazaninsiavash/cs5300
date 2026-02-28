from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bookings import views as booking_views
from django.contrib.auth import views as auth_views

# register all 3 viewsets with the router
router = DefaultRouter()
router.register(r'movies', booking_views.MovieViewSet, basename='movie')
router.register(r'seats', booking_views.SeatViewSet, basename='seat')
router.register(r'bookings', booking_views.BookingViewSet, basename='booking')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('', booking_views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/book/', booking_views.seat_booking, name='book_seat'),
    path('history/', booking_views.booking_history, name='booking_history'),
    path('bookings/<int:booking_id>/cancel/', booking_views.cancel_booking, name='cancel_booking'),
    path('login/', auth_views.LoginView.as_view(template_name='bookings/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', booking_views.signup, name='signup'),
]