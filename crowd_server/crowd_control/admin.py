from django.contrib import admin

from . models import HostDetail, Room, Track, VoterDetail

# Register your models here.
admin.site.register(HostDetail)
admin.site.register(Room)
admin.site.register(Track)
admin.site.register(VoterDetail)
