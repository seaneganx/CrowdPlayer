from django.http import HttpResponse

def index(request):
	return HttpResponse("CrowdPlayer is currently in development.")
