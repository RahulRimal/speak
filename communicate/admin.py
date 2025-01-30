from django.contrib import admin

from communicate.models import Participant, Room

# Register your models here.


admin.site.register(Room)

admin.site.register(Participant)