from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import EventPlanner, PreviousWork, WorkImages

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('id', 'name', 'email', 'role')
    list_filter = ('role',)
    ordering = ('id',)
    fieldsets = [
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'role', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
        ('Other', {'fields': ('otp', 'activation_key')}),
    ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'role', 'gender', 'img'),
        }),
    )


# @admin.register(PreviousWork)
# class PreviousWorkAdmin(admin.ModelAdmin):
#     # Customize the display fields in the admin list view
#     list_display = ('id', 'event_planner', 'title', 'date', 'capacity', 'event_type')
#     # Add filter functionality for the specified fields
#     list_filter = ('event_planner', 'date', 'event_type')
#     # Add search functionality for the specified fields
#     search_fields = ('event_planner__username', 'title', 'description')
#
#     # Define a nested inline admin for WorkImages
#     class WorkImagesInline(admin.TabularInline):
#         model = WorkImages
#
#     # Include the nested inline admin in the PreviousWork admin view
#     inlines = [WorkImagesInline]

class WorkImagesInline(admin.TabularInline):
    model = WorkImages


class PrevInline(admin.TabularInline):
    model = PreviousWork


@admin.register(EventPlanner)
class EventPlannerAdmin(admin.ModelAdmin):
    model = EventPlanner
    list_display = ('id', 'name', 'email', 'role')
    list_filter = ('role',)
    ordering = ('id',)
    inlines = [PrevInline]


@admin.register(PreviousWork)
class PreviousWorkAdmin(admin.ModelAdmin):
    model = PreviousWork
    list_display = ('id', 'event_planner', 'title', 'date', 'capacity', 'event_type')
    inlines = [WorkImagesInline]


@admin.register(WorkImages)
class WorkImagesAdmin(admin.ModelAdmin):
    model = WorkImages
    list_display = ('id', 'prev_work', 'display_image')

    def prev_work(self, obj):
        return obj.previous_work.title

    def display_image(self, obj):
        return format_html('<img src="{}" height="70px" width="50px"/>', obj.image.url)

    display_image.short_description = 'Image'
