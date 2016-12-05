from django.contrib import admin

from . models import Host, Room, Track

# Register your models here.
admin.site.register(Host)
admin.site.register(Room)
admin.site.register(Track)
