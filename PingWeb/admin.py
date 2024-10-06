from django.contrib import admin
from .models import Participant
from .models import Reservation

# Register your models here.
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('cin', 'email', 'first_name', 'last_name', 'username', 'participant_category', 'created_at','updated_at')

admin.site.register(Participant, ParticipantAdmin)

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('conference', 'participant', 'confirmed', 'reservation_date')

admin.site.register(Reservation, ReservationAdmin)