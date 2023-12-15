from rest_framework import permissions
from django.db.models import Q
from .models import Blocklist

class NotBlockedPermission(permissions.BasePermission):
    """
    Global permission check for blocked IPs and accounts.
    """

    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']
        blocked = Blocklist.objects.filter(Q(ip_addr=ip_addr) | Q(user=request.user)).exists()
        return not blocked