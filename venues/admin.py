from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from .models import Venue, VenueImages, LegalDocuments, VenueBooking


@admin.register(VenueBooking)
class VenueBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'venue', 'user', 'total_price')


@admin.register(LegalDocuments)
class LegalDocumentsAdmin(admin.ModelAdmin):
    list_display = ('venue', 'tax_card',
                    'commercial_register',
                    'license_agreement',
                    'rental_contract',
                    'ownership_contract',
                    'national_id')


@admin.register(VenueImages)
class VenueImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_image', 'image')

    def display_image(self, obj):
        image_url = self.get_full_image_url(obj)
        return format_html('<a href="{0}">{0}</a>', image_url)

    display_image.short_description = 'Image URL'

    def get_full_image_url(self, obj):
        # Replace 'your-cloudinary-url' with your actual Cloudinary URL
        cloudinary_url = 'https://res.cloudinary.com/dn6wxyqha/image/upload/v1/'
        image_path = str(obj.image)
        full_image_url = cloudinary_url + image_path
        return full_image_url


class LegalDocumentsInline(admin.StackedInline):
    model = LegalDocuments


class VenueImagesInline(admin.TabularInline):
    model = VenueImages


# Register your models here.
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'view_owner_link', 'city', 'status', 'price_per_hour', 'show_total_bookings')
    list_display_links = ('name',)
    list_filter = ('status',)
    inlines = [LegalDocumentsInline, VenueImagesInline]

    def show_total_bookings(self, obj):
        from django.db.models import Sum
        try:
            total = VenueBooking.objects.filter(venue=obj).aggregate(Sum('total_price'))
            return total['total_price__sum']
        except VenueBooking.DoesNotExist:
            return 0

    def view_owner_link(self, obj):
        url = reverse('admin:accounts_user_changelist') + f'{obj.owner.id}/change/?' + urlencode(
            {"user_id": f"{obj.owner.id}"})
        return format_html(f'<a href="{url}">{obj.owner}</a>')

    show_total_bookings.short_description = "Total Booking Price"
    view_owner_link.short_description = "owner"



