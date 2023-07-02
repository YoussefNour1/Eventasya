from django.contrib import admin

# Register your models here.
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from events.models import Event, EventBooking


@admin.register(Event)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'view_owner_link', 'city', 'is_approved', 'show_total_bookings')
    list_display_links = ('name', )
    list_filter = ('is_approved', 'city', )

    def show_total_bookings(self, obj):
        from django.db.models import Sum
        try:
            total = EventBooking.objects.filter(event=obj).aggregate(Sum('total_price'))
            return total['total_price__sum']
        except EventBooking.DoesNotExist:
            return 0

    def view_owner_link(self, obj):
        url = reverse('admin:accounts_user_changelist') + f'{obj.user.id}/change/?' + urlencode({"user_id": f"{obj.user.id}"})
        return format_html(f'<a href="{url}">{obj.user}</a>')
    show_total_bookings.short_description = "Total Booking Price"
    view_owner_link.short_description = "user"

