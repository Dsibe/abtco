from django.contrib import admin
from django.urls import path, include
import datetime

from main.views import *
from users.views import *
from django.contrib.auth import views as auth_views
from users.models import *
# Startup

# Должно быть типа request.user
def add_unlocked(user):
    if int(user.unlocked) < 15:
        if int(user.unlocked) <= 2:
            unlocked = int(user.unlocked) + 1
            user.unlocked = unlocked
            print(user.unlocked, user)
            user.save()
            # print('Free')
        elif int(user.unlocked) >= 3:
            if user.ppaid == True:
                unlocked = int(user.unlocked) + 1
                user.unlocked = unlocked
                # print(user.unlocked, user)
                user.save()
                # print('Paid')


for user in Profile.objects.all():
    day = datetime.datetime.today().weekday()
    if day == 0 or day == 3:
        add_unlocked(user)


# print('URLS')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('paypal/', include('paypal.standard.ipn.urls')),
    path('process-payment/<str:course>/', process_payment, name='process_payment'),
    path('payment-done/', payment_done, name='payment_done'),
    path('payment-cancelled/', payment_canceled, name='payment_cancelled'),

    path('', main, name='main'),
    path('path/<str:slug>/', post_detail, name='post_detail_url'),
    path('departments', departments, name='departments'),
    path('junior-studio/', junior_studio, name="junior-studio"),
    path('trading/', trading, name='trading'),
    path('trading-ru/', trading_ru, name='trading-ru'),
    path('trading-en/', trading_en, name='trading-en'),
    path('trading-ua/', trading_ua, name='trading-ua'),
    path('trading-es/', trading_es, name='trading-es'),
    path('trading-fr/', trading_fr, name='trading-fr'),

    path('trading-ru-i/', trading_ru_i, name='trading-ru-i'),
    path('trading-ru-g/', trading_ru_g, name='trading-ru-g'),
    path('trading-fr-i/', trading_fr_i, name='trading-fr-i'),
    path('trading-es-i/', trading_es_i, name='trading-es-i'),
    path('trading-en-i/', trading_en_i, name='trading-en-i'),
    path('trading-ua-i/', trading_ua_i, name='trading-ua-i'),
    path('trading-fr-g/', trading_fr_g, name='trading-fr-g'),
    path('trading-es-g/', trading_es_g, name='trading-es-g'),
    path('trading-en-g/', trading_en_g, name='trading-en-g'),
    path('trading-ua-g/', trading_ua_g, name='trading-ua-g'),

    path('developing/', developing, name="developing"),
    path('contact-us/', contact_us, name="contact-us"),
    path('fuel-additives/', fuel_additives, name="fuel-additives"),
    path('websites-developing/', websites_developing, name="websites-developing"),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='loginn'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
]
