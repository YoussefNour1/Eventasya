from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from .models import Event
from .serializers import EventSerializer, TicketSerializer, FavouriteEventSerializer  # EventBookingSerializer


class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['city', 'type']
    search_fields = ['name', 'date']
    order_fields = ['date', 'start_time']


class EventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny, ]


class TicketsListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        event = Event.objects.get(pk=self.kwargs['eventId'])
        return event.ticket_set.all()

    def post(self, request, *args, **kwargs):
        event = Event.objects.get(pk=self.kwargs['eventId'])
        tickets_data = request.data.get('tickets', [])

        tickets = []
        with transaction.atomic():
            for ticket_data in tickets_data:
                serializer = self.get_serializer(data=ticket_data)
                serializer.is_valid(raise_exception=True)
                ticket = serializer.save(event=event)
                tickets.append(ticket)

        return Response(TicketSerializer(tickets, many=True), status=status.HTTP_201_CREATED)


class FavouriteEventView(generics.ListCreateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FavouriteEventSerializer

    def get_queryset(self):
        user = self.request.user
        return user.favouriteevent_set.all()

    def delete(self, request, *args, **kwargs):
        user = request.user
        event = Event.objects.get(self.kwargs['eventId'])
        user.favouriteevent_set.remove(event)
        return user.favouriteevent_set.all()


# class EventBookAPIView(generics.ListCreateAPIView):
#     serializer_class = EventBookingSerializer
#     permission_classes = [IsAuthenticated, ]
#
#     def get_queryset(self):
#         user = self.request.user
#         return user.eventbooking_set.all()
#
#     def post(self, request, *args, **kwargs):
#         user = self.request.user
