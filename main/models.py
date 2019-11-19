from django.db import models

# Create your models here.


class Dates(models.Model):
    dates = models.CharField(max_length=10000, blank=True, null=True)

    def __str__(self):
        return self.dates
