from rest_framework import permissions

class IsHost(permissions.BasePermission):
	def has_permission(self, request, view):

		# hosts can make this request
		if hasattr(request.user, 'host'):
			return True

		# everybody else is not allowed
		return False

class IsHostOrReadOnly(permissions.BasePermission):
	def has_permission(self, request, view):

		# any can make this request if it's read-only
		if request.method in ['GET', 'HEAD', 'OPTIONS']:
			return True

		# hosts can make this request
		elif IsHost.has_permission(self, request, view):
			return True

		# everybody else is not allowed
		return False
