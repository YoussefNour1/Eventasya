from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


def upload(instance, filename):
    return f'events/images/{instance.name}/{filename}'


class Event(models.Model):
    name = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()
    event_pic = models.ImageField(max_length=200, null=True, blank=True, upload_to=upload)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.TextField()
    city = models.CharField(max_length=100)
    date = models.DateField(default=timezone.datetime.now)
    type = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    contact_number = models.CharField(max_length=12)
    pypal_number = models.CharField(max_length=12, null=True, blank=True)
    pypal_email = models.CharField(max_length=100, null=True, blank=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.type


class PaymentType(models.TextChoices):
    IN_PERSON = ("in-person", "In-Person")
    ONLINE = ("online", "ONLINE")


class EventBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(choices=PaymentType.choices, max_length=10)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)


class FavouriteEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favouriteEvents')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
