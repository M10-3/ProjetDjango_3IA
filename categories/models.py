from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
def validate_letters_only(value):
    if not re.match(r'^[A-Za-z\s]+$', value) :
        raise ValidationError('this field should only contain letters')

#On a plusieurs manière d'utiliser les validators 
#title= models.CharField(max_length=255, validators=[RegexValidator]) comme ici le faire directement
# Create your models here.
class Category (models.Model) : 
    letters_only = RegexValidator(r'^[A-Za-z\s]+$', 'Only letters are allowed')#ou de cette manière
    title= models.CharField(max_length=255, validators=[letters_only])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta :
        verbose_name_plural = "categories"