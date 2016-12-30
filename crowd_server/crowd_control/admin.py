from django.contrib import admin

from . models import *

# Register your models here.
admin.site.register(Host)
admin.site.register(Room)
admin.site.register(Track)
admin.site.register(Voter)
admin.site.register(TrackVote)
