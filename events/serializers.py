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
        read_only_fields =['user', ]

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
    ticket_type = serializers.CharField(source='ticket.type', read_only=True)
    ticket_price = serializers.DecimalField(source='ticket.price', max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = EventBooking
        fields = ['event', 'event_name', 'ticket', 'ticket_type', 'ticket_price', 'quantity', 'total_price',
                  'payment_type']
        read_only_fields = ['event_name', 'ticket_type', 'ticket_price', 'total_price']

    def validate(self, attrs):
        quantity = attrs['quantity']
        price = self.instance.ticket.price  # Access ticket price from the related ticket instance
        attrs['total_price'] = price * quantity
        return attrs

