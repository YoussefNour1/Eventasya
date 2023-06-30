from datetime import datetime, timedelta
from decimal import Decimal

from rest_framework import serializers
from .models import Venue, VenueImages, LegalDocuments, VenueBooking, Review, FavouriteVenues


class VenueImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenueImages
        fields = ('id', 'image')


class LegalDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalDocuments
        fields = ('id', 'tax_card', 'commercial_register', 'license_agreement',
                  'rental_contract', 'ownership_contract', 'national_id')


class VenueSerializer(serializers.ModelSerializer):
    venue_images = VenueImagesSerializer(many=True, read_only=True)
    legal_documents = LegalDocumentsSerializer(read_only=True)
    status = serializers.ReadOnlyField()

    class Meta:
        model = Venue
        fields = ('id', 'name', 'owner', 'address', 'city', 'description', 'category',
                  'price_per_hour', 'start_time', 'end_time', 'fits_with', 'min_capacity',
                  'max_capacity', 'facilities', 'status', 'view_type', 'venue_images',
                  'legal_documents')


class VenueBookingSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    # user = serializers.ReadOnlyField()

    class Meta:
        model = VenueBooking
        fields = '__all__'

    def create(self, validated_data):
        venue = validated_data['venue']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        start_time = validated_data['start_time']
        end_time = validated_data['end_time']

        # Check if the venue is already booked for the specified date and time range
        conflicting_bookings = VenueBooking.objects.filter(
            venue=venue,
            start_date__lte=end_date,
            end_date__gte=start_date,
            start_time__lte=end_time,
            end_time__gte=start_time,
        )
        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = datetime.combine(end_date, end_time)

        if conflicting_bookings.exists():
            raise serializers.ValidationError("This venue is already booked for the specified date and time range.")

        open_hour = venue.start_time

        if start_time < open_hour:
            print(start_datetime, " ", end_datetime)
            raise serializers.ValidationError("This venue can't be booked as there's a conflict with working hours.")

        # Calculate the duration and total price

        duration = (end_datetime - start_datetime).total_seconds() / 3600
        price_per_hour = float(venue.price_per_hour)
        total_price = price_per_hour * duration

        validated_data['total_price'] = Decimal(total_price)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Check if the venue is already booked for the specified date and time range
        conflicting_bookings = VenueBooking.objects.filter(
            venue=instance.venue,
            start_date__lte=validated_data.get('end_date', instance.end_date),
            end_date__gte=validated_data.get('start_date', instance.start_date),
            start_time__lte=validated_data.get('end_time', instance.end_time),
            end_time__gte=validated_data.get('start_time', instance.start_time),
        ).exclude(user=instance.user)

        if conflicting_bookings.exists():
            raise serializers.ValidationError("This venue is already booked for the specified date and time range.")

        # Update the start and end time fields
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.end_time = validated_data.get('end_time', instance.end_time)

        # Recalculate the total price
        start_datetime = datetime.combine(instance.start_date, instance.start_time)
        end_datetime = datetime.combine(instance.end_date, instance.end_time)

        # Adjust the end_datetime if it is on a subsequent day
        if instance.end_time < instance.start_time:
            end_datetime += timedelta(days=1)

        duration = (end_datetime - start_datetime).total_seconds() / 3600
        price_per_hour = float(instance.venue.price_per_hour)
        total_price = price_per_hour * duration

        instance.total_price = Decimal(total_price)

        instance.save()
        return instance


class VenueOwnerVenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'


class VenueOwnerBookingSerializer(serializers.ModelSerializer):
    venue = VenueOwnerVenueSerializer()

    class Meta:
        model = VenueBooking
        fields = '__all__'


class UserBookingSerializer(serializers.ModelSerializer):
    venue = VenueSerializer()

    class Meta:
        model = VenueBooking
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


# class FavouriteVenuesSerializer(serializers.ModelSerializer):
#     venue = VenueSerializer(many=True)
#
#     class Meta:
#         model = FavouriteVenues
#         fields = ['venue']
