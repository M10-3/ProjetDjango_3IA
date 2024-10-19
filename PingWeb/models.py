from django.db import models
from django.contrib.auth.models import AbstractUser
from conferences.models import Conferences
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


def email_validator(value) :
    if not value.endswith('@esprit.tn'):
        raise ValidationError('Email Invalid, only @esprit.tn domain are allowed')
    
# Create your models here.
class Participant (AbstractUser) : 
    cin_validator = RegexValidator(regex=r'^\d{8}$', message="this field must contain exactly 8 digits")
    cin= models.CharField(primary_key= True, max_length=8, validators=[cin_validator])
    email = models.EmailField(unique=True, max_length=255, validators=[email_validator])
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(unique=True,max_length=255)
    USERNAME_FIELD='username'#Pour declarer à django que le champ d'authentification est username
    CHOICES=(
       ('etudiant', 'etudiant'),
       ('chercheur', 'chercheur'),
       ('docteur', 'docteur'),
       ('enseignant', 'enseignant'),
    )
    participant_category = models.CharField(max_length=255, choices=CHOICES)#Une liste de choix
    reservations = models.ManyToManyField(Conferences, through='Reservation', related_name='reservations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta :
        verbose_name_plural = "participants"

class Reservation(models.Model) :
    conference= models.ForeignKey(Conferences, on_delete=models.CASCADE)
    participant= models.ForeignKey(Participant, on_delete=models.CASCADE)   
    confirmed=models.BooleanField(default=False)
    reservation_date= models.DateTimeField(auto_now_add=True)
    def clean(self) :
        if self.conference.start_date < timezone.now().date(): 
            raise ValidationError('you can only reserve for upcomming conference')
        today = timezone.now().date()
        reservation_count = Reservation.objects.filter(participant = self.participant, reservation_date__date = today).count()
        if reservation_count >= 3 :
            raise ValidationError('You can only have 3 reservations')
    class Meta :
        unique_together=('conference', 'participant')
        verbose_name_plural = "reservations"
