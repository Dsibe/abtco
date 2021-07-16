import datetime
import calendar
import os
import telebot
import datetime
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from sellapp.models import License
from .models import App

from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import (invalid_ipn_received,
                                         valid_ipn_received)
from paypal.standard.models import ST_PP_COMPLETED


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def debug_env_var(name):
    try:
        with open(
                rf'D:\libraries\Desktop\Dj\env\Scripts\app\abtco_env\{name}.txt'
        ) as file:
            return file.read()
    except:
        pass


TOKEN = os.environ.get('tg_token', debug_env_var('tg_token'))
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = int(os.environ.get('admin_id', debug_env_var('admin_id')))


def show_app(request, name_id):
    apps = App.objects.filter(name_id=name_id)

    if apps.exists():
        app = apps[0]
        app.views_amount += 1
        app.save()

        app.videos_json = json.loads(app.videos)
        app.screenshots_json = json.loads(app.screenshots)
        app.faq_json = json.loads(app.faq)
        app.pricing_json = json.loads(app.pricing)

        return render(request, 'shop/app.html', context={'app': app})
    return render(request, 'shop/404.html')


def login_or_signup(request):
    return render(request,
                  'shop/login_or_signup.html',
                  context={'next': request.GET.get('next')})


@login_required(login_url='/login-or-signup')
def buy_license(request, app_name_id, pricing_id, period, max_machines_amount):
    app = App.objects.get(name_id=app_name_id)
    pricing = json.loads(app.pricing)
    plan = [i for i in pricing if i['pricing_id'] == pricing_id][0]

    host = request.get_host()
    username = request.user.username

    if plan['is_custom']:
        price = calc_custom_price(plan, period, max_machines_amount)
    else:
        price = plan['price']
        period = plan['period']
        max_machines_amount = plan['max_machines_amount']

    price = f'{price:.2f}'
    period_paypal = 'forever' if not period else f'{period} months'

    item_name = f"{username} - {app.name} {period_paypal}"
    invoice = f'{item_name} {datetime.datetime.now()}'

    custom = [
        username, app.name_id, plan['pricing_id'], period, max_machines_amount
    ]
    custom = json.dumps(custom)

    paypal_dict = {
        "business": receiver_email,
        "amount": str(price),
        "item_name": item_name,
        "currency_code": "USD",
        "invoice": invoice,
        "notify_url": f"http://{host}{reverse('paypal-ipn')}",
        "return_url": f"http://{host}{reverse('payment_done')}",
        "cancel_return": f"http://{host}{reverse('payment_cancelled')}",
        "custom": custom,
    }

    form = PayPalPaymentsForm(initial=paypal_dict)

    return render(request,
                  'shop/payment_preview.html',
                  context={
                      'app': app,
                      'plan': plan,
                      'form': form,
                      'price': price,
                      'period': period,
                      'max_machines_amount': max_machines_amount,
                  })


def calc_custom_price(plan, months_amount, machines_amount):
    if months_amount > 3:
        discount_percent = 0.15
    elif months_amount > 6:
        discount_percent = 0.30
    elif months_amount > 12:
        discount_percent = 0.60
    else:
        discount_percent = 0

    months_total_sum = (months_amount * 3)
    months_total_sum = months_total_sum * (1 - discount_percent)

    machines_amount = machines_amount * (1 - discount_percent)
    machines_total_sum = months_total_sum * machines_amount

    machines_total_sum *= plan['custom_multiplier']

    return round(machines_total_sum, 2)


receiver_email = 'abt.company-facilitator@aol.com'


def process_payment(sender, **kwargs):
    print()
    print('process_payment')

    ipn_obj = sender

    if ipn_obj.payment_status == ST_PP_COMPLETED:
        print("Received payment, processing")

        if ipn_obj.receiver_email != receiver_email:
            return

        if ipn_obj.business != receiver_email:
            return

        custom = ipn_obj.custom
        username, app_name_id, pricing_id, period, max_machines_amount = json.loads(
            custom)

        user = User.objects.get(username=username)
        app = App.objects.get(name_id=app_name_id)
        pricing = json.loads(app.pricing)
        plan = [i for i in pricing if i['pricing_id'] == pricing_id][0]

        if not plan['is_custom']:
            period = plan['period']
            max_machines_amount = plan['max_machines_amount']

            if float(ipn_obj.payment_gross) != plan['price']:
                return
        else:
            if float(ipn_obj.payment_gross) != calc_custom_price(
                    plan, period, max_machines_amount):
                return

        if ipn_obj.mc_currency != 'USD':
            return

        license = License(user=user,
                          product=app,
                          expiration=period,
                          max_machines_limit=max_machines_amount,
                          creation_date=datetime.date.today())

        license.create_key()
        license.save()

        client_data = str(ipn_obj.posted_data_dict)
        bot.send_message(ADMIN_ID, client_data)
        print("Received payment, done")
    else:
        print("Failed")


valid_ipn_received.connect(process_payment)
invalid_ipn_received.connect(process_payment)


@csrf_exempt
def payment_done(request):
    return render(request, "shop/payment_done.html")


@csrf_exempt
def payment_canceled(request):
    return render(request, 'shop/payment_cancelled.html')


def main(request):
    apps = App.objects.all()
    for app in apps:
        pricing = json.loads(app.pricing)
        from_prices = [i['price'] for i in pricing if not i['is_custom']]
        app.from_price = min(from_prices)

    return render(request, 'shop/main.html', context={'apps': apps})


def login(request):
    context = {}
    if request.GET.get('next') is None:
        context = {'next': '/profile'}

    return render(request, 'shop/login.html', context=context)


def contact_us(request):
    return render(request, 'shop/contact_us.html')


def register(request):
    next = request.GET.get('next')
    next = next if next else '/profile'

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            return redirect(f'/login?next={next}')
    else:
        form = UserRegisterForm()

    return render(request,
                  "shop/register.html",
                  context={
                      "form": form,
                      'next': next
                  })


@login_required(login_url='/login-or-signup')
def profile(request):
    user = User.objects.get(username=request.user.username)
    licenses = user.license_set.all()

    for license in licenses:
        expiration_date = add_months(license.creation_date, license.expiration)
        license.end_of_license = expiration_date

    return render(request, 'shop/profile.html', context={"licenses": licenses})


def logout(request):
    return render(request, 'shop/logout.html')


@login_required(login_url='/login-or-signup')
def update_profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST)

        if form.is_valid():
            user = request.user
            user.username = form.cleaned_data['new_username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            return redirect("shop_profile")
    else:
        user = request.user
        form = UserUpdateForm(instance=user,
                              initial={'new_username': user.username})

    return render(request, "shop/update_profile.html", context={"form": form})
