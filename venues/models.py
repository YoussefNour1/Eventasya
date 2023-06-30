from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from accounts.models import VenueOwner

User = get_user_model()


def file_upload_to(instance, filename):
    return 'venues/legalDocs/{venue}/{filename}'.format(venue=instance.venue.id, filename=filename)


def venue_image_upload_to(instance, filename):
    return 'venues/images/{venue}/{filename}'.format(venue=instance.venue.id, filename=filename)


class Categories(models.TextChoices):
    RELIGIOUS = "religious", "Religious"
    OPEN_AIR = "openair", "Open Air"
    YACHT = "yacht", "Yacht"
    CONFERENCE = "conference", "Conference"
    CLASS_HAll = "class hall", "Class Hall"


class Venue(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(VenueOwner, on_delete=models.CASCADE, related_name='owned_venues')
    address = models.TextField()
    city = models.CharField(max_length=50)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=Categories.choices)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField(default=timezone.datetime.now, null=True, blank=True)
    end_date = models.DateField(default=timezone.datetime.now, null=True, blank=True)
    fits_with = models.CharField(max_length=25)
    min_capacity = models.PositiveIntegerField()
    max_capacity = models.PositiveIntegerField()
    facilities = models.TextField()
    view_type = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=[("active", "Active"), ("suspended", "Suspended")], default="suspended")
    rate = models.DecimalField(decimal_places=2, max_digits=4, default=0)

    def __str__(self):
        return self.name


class LegalDocuments(models.Model):
    venue = models.OneToOneField('Venue', on_delete=models.CASCADE, related_name="legalDocs")
    tax_card = models.FileField(upload_to=file_upload_to, null=True, blank=True)
    commercial_register = models.FileField(upload_to=file_upload_to, null=True, blank=True)
    license_agreement = models.FileField(upload_to=file_upload_to, null=True, blank=True)
    rental_contract = models.FileField(upload_to=file_upload_to, null=True, blank=True)
    ownership_contract = models.FileField(upload_to=file_upload_to, null=True, blank=True)
    national_id = models.FileField(upload_to=file_upload_to, null=True, blank=True)

    def __str__(self):
        return f'{self.venue.name}'


class VenueImages(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="venue_images")
    image = models.ImageField(upload_to=venue_image_upload_to)


STATUS = [
    ("approved", "Approved"),
    ("pending", "Pending"),
    ("rejected", "Rejected")
]


class PaymentMethods(models.TextChoices):
    IN_PERSON = ('in-person', 'In-Person')
    ONLINE = ('online', 'Online')


class VenueBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    payment_type = models.CharField(max_length=50, choices=PaymentMethods.choices)
    note = models.TextField(null=True, blank=True)
    event_type = models.CharField(max_length=50)
    request_status = models.CharField(max_length=50, choices=STATUS, default='pending')
    total_price = models.DecimalField(max_digits=8, decimal_places=2)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    rating = models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=Review)
def update_venue_rate(sender, instance, **kwargs):
    venue = instance.venue
    new_rate = Review.objects.filter(venue=venue).aggregate(rate_avg=Avg('rate'))['rate_avg']
    venue.rate = new_rate
    venue.save()


class FavouriteVenues(models.Model):
    user = models.ManyToManyField(User, related_name="favouriteVenues")
    venue = models.ManyToManyField(Venue)
