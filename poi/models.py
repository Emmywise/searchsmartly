from django.db import models

# Create your models here.

from django.db import models

class PointOfInterest(models.Model):
    internal_id = models.AutoField(primary_key=True)
    external_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    category = models.CharField(max_length=255)
    average_rating = models.FloatField()

    def __str__(self):
        return self.name
