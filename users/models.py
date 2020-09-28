import re
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from random import randint
from uuid import uuid4
from django.shortcuts import reverse
import datetime
from django.contrib.auth.decorators import login_required


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unlocked = models.CharField(max_length=15,
                                blank=True,
                                null=True,
                                default=1)
    ppaid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)


def gen_slug():
    return slugify(
        str(randint(1, 1000000000000000)) + str(uuid4()) +
        str(datetime.datetime.now()))


class Post(models.Model):
    title = models.CharField(max_length=164, null=True)
    slug = models.SlugField(max_length=400,
                            unique=True,
                            null=True,
                            blank=True,
                            default=gen_slug())
    body = models.TextField(max_length=100000)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})
    
    def change_urls(self):
        pattern = r'<img src="http://code-d.000webhostapp.com/.*">'
        new_body = re.sub(pattern, )