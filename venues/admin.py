from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from .models import Venue, VenueImages, LegalDocuments, VenueBooking


# Register your models here.
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'view_owner_link', 'city', 'status', 'price_per_hour', 'show_total_bookings')
    list_display_links = ('name', )
    list_filter = ('status',)
    def show_total_bookings(self, obj):
        from django.db.models import Sum
        try:
            total = VenueBooking.objects.filter(venue=obj).aggregate(Sum('total_price'))
            return total['total_price__sum']
        except VenueBooking.DoesNotExist:
            return 0

    def view_owner_link(self, obj):
        url = reverse('admin:accounts_user_changelist') + f'{obj.owner.id}/change/?' + urlencode({"user_id": f"{obj.owner.id}"})
        return format_html(f'<a href="{url}">{obj.owner}</a>')
    show_total_bookings.short_description = "Total Booking Price"
    view_owner_link.short_description = "owner"


admin.site.register(VenueImages)


@admin.register(LegalDocuments)
class LegalDocuments(admin.ModelAdmin):
    list_display = ('venue', 'tax_card',
                    'commercial_register',
                    'license_agreement',
                    'rental_contract',
                    'ownership_contract',
                    'national_id')


@admin.register(VenueBooking)
class VenueBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'venue', 'user', 'total_price')
