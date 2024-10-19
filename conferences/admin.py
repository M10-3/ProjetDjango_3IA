from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Conferences
from PingWeb.models import Reservation
from django.db.models import Count
from django.utils import timezone

class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 1 # Nombre de lignes vides à afficher
    readonly_fields = ('reservation_date',)
    can_delete = True

class ParticipantFilter(admin.SimpleListFilter):
    title = "participant filter"
    parameter_name = "participants"
    def lookups(self, request, model_admin):
        return (('0', ('No participants')),
                ('more', ('they are participants'))
                )
    def queryset(self, request, queryset):
        if self.value()=='0':
            return queryset.annotate(participant_count = Count('reservations')).filter(participant_count = 0)
        if self.value()=='more':
            return queryset.annotate(participant_count = Count('reservations')).filter(participant_count__gt = 0)
        return queryset  

class ConferenceDateFilter(admin.SimpleListFilter):
    title = "date conference filter"
    parameter_name = "start_date"
    def lookups(self, request, model_admin):
        return (('past', 'Past Conferences'),
            ('today', 'Today Conferences'),
            ('upcoming', 'Upcoming Conferences'),
                )
    def queryset(self, request, queryset):
        today = timezone.now().date()
        if self.value() == 'past':
            return queryset.filter(start_date__lt=today)
        if self.value() == 'today':
            return queryset.filter(start_date=today)
        if self.value() == 'upcoming':
            return queryset.filter(start_date__gt=today)
        return queryset     

# Register your models here.
class ConferencesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'start_date', 'end_date', 'location', 'price', 'capacity', 'program', 'created_at', 'updated_at', 'category')
    
    search_fields = ('title',) # permet de mettre des attributs en tant que recherche 
    
    list_per_page = 2 #Pagination : c'est une technique utilisée dans le développement web et les interfaces utilisateur pour diviser une longue liste d'éléments en plusieurs pages.
    
    ordering = ('start_date',)  # Ordre par date de début
    
    fieldsets = (
        ('Description', {
            'fields': ('title', 'description', 'category')
        }),
        ('Horaires de la conférence', {
            'fields': ('start_date', 'end_date')
        }),
        ('Informations sur le lieu', {
            'fields': ('location', 'capacity', 'price')
        }),
        ('Documents', {
            'fields': ('program',)
        }),
        ('Statistiques', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Permet de réduire la section
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')  # Champs en lecture seule c'est-à-dire ne pas le rendre modifiable

    inlines = [ReservationInline] # Ajout de l'inline pour les réservations

    autocomplete_fields = ('category',) #Permet de mettre dans l'administration Django une barre de recherche (dans notre cas la table categories et conferences)

    list_filter = (
        'title', ParticipantFilter, ConferenceDateFilter
    )
admin.site.register(Conferences, ConferencesAdmin)