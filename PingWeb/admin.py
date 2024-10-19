from django.contrib import admin
from .models import Participant
from .models import Reservation
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
import datetime
from django.utils.timezone import now
from django.db import models
import csv
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages

class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 1  # Nombre de réservations vierges à ajouter par défaut

#filtrer les participants selon s'ils ont fait des réservations ou non.
class ReservationStatusFilter(SimpleListFilter):
    title = 'Reservation Status'  # Le titre qui apparaîtra dans l'interface admin
    parameter_name = 'has_reservations'  # Le nom du paramètre de requête

    def lookups(self, request, model_admin):
        # Retourne les options de filtrage (affiché sous forme de dropdown)
        return (
            ('has', 'Has Reservations'),
            ('has_not', 'No Reservations'),
        )

    def queryset(self, request, queryset):
        # Filtre les participants qui ont ou n'ont pas de réservations
        if self.value() == 'has':
            return queryset.filter(reservations__isnull=False).distinct()
        if self.value() == 'has_not':
            return queryset.filter(reservations__isnull=True)

#filtrer par date, par exemple les participants créés cette semaine, ce mois-ci, ou cette année.
class CreatedAtFilter(SimpleListFilter):
    title = 'Date Created'  # Le titre du filtre
    parameter_name = 'created_at_range'  # Le nom du paramètre

    def lookups(self, request, model_admin):
        # Les options du filtre
        return (
            ('today', 'Today'),
            ('this_week', 'This Week'),
            ('this_month', 'This Month'),
        )

    def queryset(self, request, queryset):
        today = now().date()
        if self.value() == 'today':
            return queryset.filter(created_at__date=today)
        if self.value() == 'this_week':
            start_of_week = today - datetime.timedelta(days=today.weekday())  # Début de la semaine
            return queryset.filter(created_at__date__gte=start_of_week)
        if self.value() == 'this_month':
            return queryset.filter(created_at__year=today.year, created_at__month=today.month)


# Register your models here.
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('cin', 'email', 'first_name', 'last_name', 'username', 'participant_category', 'created_at','updated_at')

    list_filter = (ReservationStatusFilter, CreatedAtFilter, 'participant_category')
    search_fields = ('cin', 'email', 'first_name', 'last_name', 'username')
    inlines = [ReservationInline]  # Ajout de la gestion des réservations
    list_editable = ('participant_category',)
    readonly_fields = ('created_at', 'updated_at')
    list_display_links = ('cin', 'username')
    list_per_page = 2
    date_hierarchy = 'created_at'
    #exclude = ('last_name',)
    #fields = ('cin', 'first_name', 'last_name', 'username', 'email', 'participant_category', 'created_at','updated_at')
    #prepopulated_fields = {'slug' : ('username',)}
    #autocomplete_fields = ('cin', 'first_name', 'last_name', 'username', 'email', 'participant_category', 'created_at','updated_at')

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('cin', 'first_name', 'last_name', 'username', 'email')
        }),
        ('Informations externes', {
            'fields': ('participant_category',)
        }),
        ('Horaires', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Permet de réduire la section
        }),
    )

    #PARTIE IMPORTANTE POUR LEXPORTATION CSV
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=participants.csv'
        
        writer = csv.writer(response)
        writer.writerow(['CIN', 'Email', 'First Name', 'Last Name', 'Username', 'Category'])
        
        for participant in queryset:
            writer.writerow([participant.cin, participant.email, participant.first_name, participant.last_name, participant.username, participant.participant_category])
        
        return response

    export_as_csv.short_description = "Export selected participants as CSV"


    actions = ['send_email_notification']

    def send_email_notification(self, request, queryset):
        for participant in queryset:
            send_mail(
                'Notification from Your Application',
                'Hello, this is a notification about your account.',
                'gnine.diarra@esprit.tn', #C'est mon adresse email configuré par google
                [participant.email],
                fail_silently=False,
            )
        messages.success(request, "Emails sent successfully to selected participants.")
    
    send_email_notification.short_description = "Send email notification to selected participants"


admin.site.register(Participant, ParticipantAdmin)




class ReservationAdmin(admin.ModelAdmin):
    list_display = ('conference', 'participant', 'confirmed', 'reservation_date')

    # Définir les actions
    actions = ['make_confirmed', 'make_not_confirmed']

    # Après definir les fonctions concernées
    def make_confirmed(self, request, queryset):
        queryset.update(confirmed=True)
        self.message_user(request, _("Selected reservations have been confirmed."))

    make_confirmed.short_description = _("Confirm selected reservations")

    def make_not_confirmed(self, request, queryset):
        queryset.update(confirmed=False)
        self.message_user(request, _("Selected reservations have been set to unconfirmed."))

    make_not_confirmed.short_description = _("Unconfirm selected reservations")
    
    """
    Django inclut un système de gestion des traductions et de localisation qui permet de rendre une application disponible dans plusieurs langues.
    La fonction _() est une abréviation pour la fonction gettext() ou ugettext() dans Django. Elle est utilisée pour marquer les chaînes de caractères à traduire.
    Donc, lorsqu'une chaîne de caractères est passée dans _(), Django sait que cette chaîne devra être traduite en fonction des fichiers de traduction fournis pour différentes langues.
    """

admin.site.register(Reservation, ReservationAdmin)