from django.contrib import admin
from users.models import *
from users.forms import *
from sellapp.models import License
from shop.models import App
# Register your models here.

admin.site.register(License)
admin.site.register(Post)
admin.site.register(App)

