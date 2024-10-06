from django.db import models
from categories.models import Category
from django.core.validators import MaxValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class Conferences (models.Model) : 
    title= models.CharField( max_length=255)
    description = models.TextField()
    start_date=models.DateField(default=timezone.now().date())
    end_date=models.DateField(default=timezone.now().date())
    location=models.CharField(max_length=255)
    price = models.FloatField(default=0.00 )
    capacity = models.IntegerField(validators=[MaxValueValidator(limit_value=900, message='capacity must be under 900')],  default=100)
    program=models.FileField(upload_to='files/', validators=
                             [FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpeg', 'jpg'], message='Only pdf, png, jpeg, jpg allowed')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name="conferences")
    def clean(self):
        if self.end_date <= self.start_date: 
            raise ValidationError('End Date must be after start date')
    class Meta :
        verbose_name_plural = "conferences"
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_date__gte=timezone.now().date()),
                name="The start date must be greater than today or equal"
            )
        ]

