from django.db import models


class App(models.Model):
    name = models.CharField(max_length=50, blank=True)
    short_description = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=20000, blank=True)
    name_id = models.CharField(max_length=50, blank=True)

    pricing = models.CharField(max_length=5000, blank=True)
    faq = models.CharField(max_length=10000, blank=True)

    logo = models.CharField(max_length=1000, blank=True)
    screenshots = models.CharField(max_length=5000, blank=True)
    videos = models.CharField(max_length=5000, blank=True)

    views_amount = models.IntegerField(default=0)
    private_creds = models.CharField(max_length=50000, blank=True)
