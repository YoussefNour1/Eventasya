from rest_framework.permissions import BasePermission, IsAuthenticated

from accounts.models import Role


class IsNormalUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == Role.USER
        return IsAuthenticated().has_permission(request, view)


class IsVenueOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == Role.VENUE_OWNER
        return IsAuthenticated().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return request.user.role == Role.VENUE_OWNER and obj.owner == request.user


class IsEventPlanner(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == Role.EVENT_PLANNER
        return IsAuthenticated().has_permission(request, view)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.ADMIN


class IsNormalUserOrVenueOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return IsNormalUser().has_permission(request, view) or IsVenueOwner().has_permission(request, view)
        return IsAuthenticated().has_permission(request, view)

class IsNormalUserOrEventPlanner(BasePermission):
    def has_permission(self, request, view):
        return IsNormalUser().has_permission(request, view) or IsEventPlanner().has_permission(request, view)
