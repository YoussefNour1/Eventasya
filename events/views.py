from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from .models import Event, EventBooking
from .serializers import EventSerializer, TicketSerializer, FavouriteEventSerializer, \
    EventBookingSerializer  # EventBookingSerializer


class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.filter(is_approved=True)
    serializer_class = EventSerializer
    permission_classes = [AllowAny, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['city', 'type']
    search_fields = ['name', 'date']
    order_fields = ['date', 'start_time']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
        return user.favouriteEvents.all().order_by('id')

    def perform_create(self, serializer):
        user = self.request.user
        event = Event.objects.get(pk=self.kwargs["pk"])
        serializer.save(user=user, event=event)

    def perform_destroy(self, instance):
        instance.delete()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serialized_data = FavouriteEventSerializer(page, many=True).data
            return self.get_paginated_response(serialized_data)
        serialized_data = FavouriteEventSerializer(queryset, many=True).data
        return Response(serialized_data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serialized_data = FavouriteEventSerializer(page, many=True).data
            return self.get_paginated_response(serialized_data)
        serialized_data = FavouriteEventSerializer(queryset, many=True).data
        return Response(serialized_data, status=status.HTTP_204_NO_CONTENT)


class EventBookAPIView(generics.ListCreateAPIView):
    serializer_class = EventBookingSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = EventBooking.objects.all()

    def get_queryset(self):
        return EventBooking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, event=Event.objects.get(pk=self.kwargs['pk']))
