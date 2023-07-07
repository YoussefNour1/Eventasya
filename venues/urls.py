from django.urls import path
from .views import (
    VenueListCreateView, SingleVenueAPIView,
    VenueImagesListCreateView, VenueBookingListCreateView,
    VenueBookingRetrieveUpdateDestroyView, VenueOwnerVenueListView,
    VenueOwnerBookingListView, UserBookingListView, VenueImagesUpdateDelete, LegalDocsCreateView,
    ReviewsListCreateView, FavouriteVenueCreateDestroyView
)

urlpatterns = [
    path('', VenueListCreateView.as_view(), name='venue-list-create'),
    path('<int:pk>/', SingleVenueAPIView.as_view(), name='venue-retrieve-update-destroy'),
    path('<int:venueId>/images/', VenueImagesListCreateView.as_view(), name='venue-images-list-create'),
    path('<int:venueId>/legaldocs/', LegalDocsCreateView.as_view(), name='venue-legaldocs-create'),
    path('images/<int:pk>/', VenueImagesUpdateDelete.as_view(), name='image-update-delete'),
    path('owner/venues/', VenueOwnerVenueListView.as_view(), name='venue-owner-venue-list'),

    path('<int:pk>/bookings/', VenueBookingListCreateView.as_view(), name='venue-booking-list-create'),
    path('owner/bookings/', VenueOwnerBookingListView.as_view(), name='venue-owner-booking-list-create'),
    path('user/bookings/', UserBookingListView.as_view(), name='user-booking-list'),
    path('user/bookings/<int:pk>/', VenueBookingRetrieveUpdateDestroyView.as_view(), name='venue-booking-details'),

    path('<int:venueId>/reviews/', ReviewsListCreateView.as_view(), name='review-list-create'),
    path('<int:venue_id>/favourites/', FavouriteVenueCreateDestroyView.as_view(), name='review-create-destroy'),
    path('favourites/', FavouriteVenueCreateDestroyView.as_view(), name='review-list'),

    # path('paypal/create/order/', views.CreateOrderViewRemote.as_view(), name='ordercreate'),
    # path('paypal/capture/order/', views.CaptureOrderView.as_view(), name='captureorder')
]
