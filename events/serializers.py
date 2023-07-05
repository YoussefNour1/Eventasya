from rest_framework import serializers
from .models import Event, Ticket, FavouriteEvent, EventBooking


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'type', 'price')


class EventSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['user', ]

    def create(self, validated_data):
        print(validated_data)
        tickets_data = validated_data.pop('tickets')
        event = Event.objects.create(**validated_data)
        try:
            for ticket_data in tickets_data:
                Ticket.objects.create(event=event, **ticket_data)
        except Exception as e:
            print(e)
        return event


class FavouriteEventSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = FavouriteEvent
        fields = ['event']


class EventBookingSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source='event.name', read_only=True)
    ticket_type = serializers.CharField(source='ticket_type.type', read_only=True)
    ticket_price = serializers.DecimalField(source='ticket_type.price', max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = EventBooking
        fields = ['id', 'event', 'event_name', 'user', 'ticket_type', 'ticket_price', 'quantity', 'total_price',
                  'payment_id']
        read_only_fields = ['event', 'user', 'event_name', 'ticket_type', 'ticket_price', 'total_price']

    def create(self, validated_data):
        event = validated_data['event']
        ticket_type = validated_data['ticket_type']
        quantity = validated_data['quantity']
        ticket_price = ticket_type.price
        total_price = ticket_price * quantity

        booking = EventBooking.objects.create(event=event, user=self.context['request'].user, ticket_type=ticket_type,
                                              quantity=quantity, total_price=total_price)

        return booking

