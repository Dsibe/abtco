from django.urls import path, include
from khatynka.views import *

urlpatterns = [
    path('', main, name='main'),
]
