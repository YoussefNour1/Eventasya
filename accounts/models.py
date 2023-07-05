from django.contrib.auth.base_user import BaseUserManager
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


def upload_to(instance, filename):
    return 'users/images/{user}.{filename}'.format(user=instance.email, filename=filename.split('.')[-1])


def upload_to_prev_work(instance, filename):
    return 'prev/images/{user}/{filename}'.format(user=instance.previous_work.event_planner, filename=filename)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        if password:
            user.set_password(password)
        else:
            user.set_password(None)
        user.save()
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Role.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Role(models.TextChoices):
    ADMIN = "admin", "Admin"
    USER = "user", "User"
    VENUE_OWNER = "venue owner", "Venue Owner"
    EVENT_PLANNER = "event planner", "Event Planner"


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=50, choices=Role.choices)
    gender = models.CharField(max_length=6, choices=[("Male", "Male"), ("Female", "Female")], blank=True, null=True)
    birthdate = models.DateField(null=True, blank=True)
    img = models.ImageField("Image", upload_to=upload_to, null=True, blank=True)
    contact_number = models.CharField(max_length=12, null=True, blank=True)
    otp = models.IntegerField(null=True, blank=True)
    activation_key = models.CharField(max_length=150, blank=True, null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        print("Saving user:", self)
        return super().save(*args, **kwargs)


# normal user model, profile and manager
class NormalUserManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=Role.USER)


class NormalUser(User):
    base_role = Role.USER
    objects = NormalUserManager()

    class Meta:
        proxy = True


# Venue Owner model, profile and manager
class VenueOwnerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=Role.VENUE_OWNER)


class VenueOwner(User):
    base_role = Role.VENUE_OWNER
    objects = VenueOwnerManager()

    class Meta:
        proxy = True


# Event Planner model, Profile and manager
class EventPlannerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=Role.EVENT_PLANNER)


class EventPlanner(User):
    base_role = Role.EVENT_PLANNER
    objects = EventPlannerManager()

    class Meta:
        proxy = True


class PreviousWork(models.Model):
    event_planner = models.ForeignKey(EventPlanner, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    date = models.DateField()
    capacity = models.PositiveIntegerField()
    event_type = models.CharField(max_length=100)


class WorkImages(models.Model):
    previous_work = models.ForeignKey(PreviousWork, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(blank=True, null=True, upload_to=upload_to_prev_work)


