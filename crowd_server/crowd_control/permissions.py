from rest_framework import permissions

class HostPermission(permissions.BasePermission):

	def has_permission(self, request, view):
		return hasattr(request.user, 'host')
