from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

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


@admin.register(PreviousWork)
class PreviousWorkAdmin(admin.ModelAdmin):
    # Customize the display fields in the admin list view
    list_display = ('id', 'event_planner', 'title', 'date', 'capacity', 'event_type')
    # Add filter functionality for the specified fields
    list_filter = ('event_planner', 'date', 'event_type')
    # Add search functionality for the specified fields
    search_fields = ('event_planner__username', 'title', 'description')

    # Define a nested inline admin for WorkImages
    class WorkImagesInline(admin.TabularInline):
        model = WorkImages

    # Include the nested inline admin in the PreviousWork admin view
    inlines = [WorkImagesInline]


@admin.register(WorkImages)
class WorkImagesAdmin(admin.ModelAdmin):
    # Customize the display fields in the admin list view
    list_display = ('id', 'previous_work', 'image')


class PreviousWorkInline(admin.TabularInline):
    model = PreviousWork


class EventPlannerAdmin(CustomUserAdmin):
    # Customize the display fields in the admin list view
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')
    # Add search functionality for the specified fields
    search_fields = ('username', 'email', 'first_name', 'last_name')
    inlines = [PreviousWorkInline]


admin.site.register(EventPlanner, EventPlannerAdmin)
# admin.site.register(PreviousWork, PreviousWorkAdmin)
# admin.site.register(WorkImages, WorkImagesAdmin)
