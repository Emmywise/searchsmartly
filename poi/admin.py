from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import PointOfInterest

@admin.register(PointOfInterest)
class PointOfInterestAdmin(admin.ModelAdmin):
    list_display = ('internal_id', 'name', 'external_id', 'category', 'average_rating')
    search_fields = ('internal_id', 'external_id')
    list_filter = ('category',)
