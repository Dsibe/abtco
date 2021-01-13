from django.db import models

# Create your models here.
class Review(models.Model):
    rating = models.FloatField()
    text = models.CharField(max_length=1500)
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    email = models.CharField(max_length=100)

class Dates(models.Model):
    dates = models.CharField(max_length=10000, blank=True, null=True)

    def __str__(self):
        return self.dates
