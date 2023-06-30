from django.urls import path

from events import views

urlpatterns = [
    path('', views.EventListCreateAPIView.as_view(), name='event-list-create'),
    path('<int:pk>', views.EventRetrieveUpdateDestroyAPIView.as_view(), name='event-get-update-delete'),
    # path('<int:pk>/bookings/', views.EventBookAPIView.as_view(), name='event-book'),
    path('<int:eventId>/tickets/', views.TicketsListCreateView.as_view(), name='tickets-list-create'),
]
