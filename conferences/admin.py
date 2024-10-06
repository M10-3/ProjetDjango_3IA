from django.contrib import admin
from .models import Conferences

# Register your models here.
class ConferencesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'start_date', 'end_date', 'location', 'program', 'created_at', 'updated_at', 'category')

admin.site.register(Conferences, ConferencesAdmin)