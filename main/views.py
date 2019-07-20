from django.shortcuts import render, redirect
from .forms import *
import datetime
from django.http import HttpResponse
from main.views import *
from users.views import *
from django.contrib.auth import views as auth_views
from users.models import *
# Startup
from os import environ



def departments(request):
    return render(request, r'main/departments.html')

def main(request):
    envir = environ
    return render(request, r'main/main.html', context={'env': envir})


def developing(request):
    return render(request, r'main/developing.html')

def junior_studio(request):
    return render(request, r'main/junior_studio.html')

def contact_us(request):
    if request.method == 'GET':
        form = ContactUsForm()
    else:
        form = ContactUsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail(f'New contact-us message from {email}, name: {name}', message, 'school@abtco.us', ['school@abtco.us', 'darik.pc@gmail.com', 'abt.company@aol.com'])
            return HttpResponse('You message has been sended succesfully')
    return render(request, r'main/contact_us.html', context={'form': form})

def trading(request):
    return render(request, r'main/trading.html')

def websites_developing(request):
    return render(request, r'main/websites_developing.html')

def fuel_additives(request):
    return render(request, r'main/fuel_additives.html')

def trading_es(request):
    return render(request, r'main/trading_es.html')

def trading_fr(request):
    return render(request, r'main/trading_fr.html')

def trading_en(request):
    return render(request, r'main/trading_en.html')

def trading_ru(request):
    return render(request, r'main/trading_ru.html')

def trading_ua(request):
    return render(request, r'main/trading_ua.html')



def trading_es_i(request):
    return render(request, r'main/trading_es_i.html')

def trading_fr_i(request):
    return render(request, r'main/trading_fr_i.html')

def trading_en_i(request):
    return render(request, r'main/trading_en_i.html')

def trading_ru_i(request):
    return render(request, r'main/trading_ru_i.html')

def trading_ua_i(request):
    return render(request, r'main/trading_ua_i.html')



def trading_es_g(request):
    return render(request, r'main/trading_es_g.html')

def trading_fr_g(request):
    return render(request, r'main/trading_fr_g.html')

def trading_en_g(request):
    return render(request, r'main/trading_en_g.html')

def trading_ru_g(request):
    return render(request, r'main/trading_ru_g.html')

def trading_ua_g(request):
    return render(request, r'main/trading_ua_g.html')
