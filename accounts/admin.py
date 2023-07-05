from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import EventPlanner, PreviousWork, WorkImages

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'role')
    list_filter = ('role',)


class EventPlannerAdmin(UserAdmin):
    # Customize the display fields in the admin list view
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')
    # Add search functionality for the specified fields
    search_fields = ('username', 'email', 'first_name', 'last_name')


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


admin.site.register(EventPlanner, EventPlannerAdmin)
# admin.site.register(PreviousWork, PreviousWorkAdmin)
# admin.site.register(WorkImages, WorkImagesAdmin)
