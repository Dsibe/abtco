import operator
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.template import Context, Template, engines
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import (invalid_ipn_received,
                                         valid_ipn_received)
from paypal.standard.models import ST_PP_COMPLETED

from .forms import *
from .models import *

django_engine = engines['django']


def thirdlesson(request):
    return redirect("process_payment")


def process_payment(request, course):

    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=request.user)
    print(type(profile))

    host = request.get_host()

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "199.99",
        "item_name": course,
        "invoice": randint(1, 10000000),
        "currency_code": "USD",
        "notify_url": "http://{}{}".format(host, reverse("paypal-ipn")),
        "return_url": "http://{}{}".format(host, reverse("payment_done")),
        "cancel_return": "http://{}{}".format(host,
                                              reverse("payment_cancelled")),
        "custom": profile,
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request,
                  "users/process_payment.html",
                  context={"form": form})


@csrf_exempt
def payment_done(request):
    return render(request, "users/payment_done.html")


@csrf_exempt
def payment_canceled(request):
    return render(request, "users/payment_cancelled.html")


def show_me_the_money(sender, **kwargs):
    ipn_obj = sender

    if ipn_obj.payment_status == ST_PP_COMPLETED:

        profile = ipn_obj.custom
        user = User.objects.get(username=profile)
        profile = Profile.objects.get(user=user)

        profile.ppaid = True
        profile.save()

        email = user.email

        send_mail(
            "You have succesfully bought course / Успешная оплата",
            "You have succesfully bought course Trading for beginners basic knowledges. You will receive 4th lesson on Thursday. It will appear in you profile. | Вы успешно оплатили курс Торговля для начинающих, Базовые знания. Вы получите 4тый урок в Четверг. Он автоматический появиться в вашем личном кабинете.",
            "abtcous2014@gmail.com",
            [email],
        )
        send_mail(
            "You have succesfully bought course / Успешная оплата",
            "You have succesfully bought course Trading for beginners basic knowledges. You will receive 4th lesson on Thursday. It will appear in you profile. | Вы успешно оплатили курс Торговля для начинающих, Базовые знания. Вы получите 4тый урок в Четверг. Он автоматический появиться в вашем личном кабинете.",
            "abtcous2014@gmail.com",
            ["darik.pc@gmail.com", "abt.company@aol.com"],
            fail_silently=False,
        )
    else:
        pass


valid_ipn_received.connect(show_me_the_money)
invalid_ipn_received.connect(show_me_the_money)


@login_required
def post_detail(request, slug):
    post = get_object_or_404(Post, slug__iexact=slug)
    body = post.body

    replace_pairs = (
        ("<r>", '<span style="color: red;">'),
        ("</r>", "</span>"),
        ("<g>", '<span style="color: #28ed12;">'),
        ("</g>", "</span>"),
        ("<b>", '<span style="color: #21409a;">'),
        ("</b>", "</span>"),
        ("<r", '<span style="color: red;">'),
        ("r>", "</span>"),
        ("<g", '<span style="color: #28ed12;">'),
        ("g>", "</span>"),
        ("<b", '<span style="color: #21409a;">'),
        ("b>", "</span>"),
        ("<R>", '<span style="color: red;">'),
        ("</R>", "</span>"),
        ("<G>", '<span style="color: #28ed12;">'),
        ("</G>", "</span>"),
        ("<B>", '<span style="color: #21409a;">'),
        ("</B>", "</span>"),
        ("<R", '<span style="color: red;">'),
        ("R>", "</span>"),
        ("<G", '<span style="color: #28ed12;">'),
        ("G>", "</span>"),
        ("<B", '<span style="color: #21409a;">'),
        ("B>", "</span>"),
    )

    for to_find, to_replace in replace_pairs:
        body = body.replace(to_find, to_replace)

    body = body.replace('http://abtco.us/', '{% static "lesson_imgs/')
    body = body.replace('http://code-d.000webhostapp.com/',
                        '{% static "lesson_imgs/')
    body = body.replace('">', '" %}">')

    new_body = f'{{% load static %}}\n{body}'
    template_body = django_engine.from_string(new_body).render()
    post.body = template_body

    context = {"post": post}
    if post.title == "3":
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user=request.user)

        host = request.get_host()

        paypal_dict = {
            "business":
            settings.PAYPAL_RECEIVER_EMAIL,
            "amount":
            "199.95",
            "item_name":
            "rug",
            "invoice":
            randint(1, 10000000),
            "currency_code":
            "USD",
            "notify_url":
            "http://{}{}".format(host, reverse("paypal-ipn")),
            "return_url":
            "http://{}{}".format(host, reverse("payment_done")),
            "cancel_return":
            "http://{}{}".format(host, reverse("payment_cancelled")),
            "custom":
            profile,
        }

        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {"post": post, "form": form, "is_third": True}
    return render(request, "users/post_detail.html", context=context)


@login_required
def profile(request):
    if request.method == "GET":
        user = request.user
        user_profile = Profile.objects.get(user=user)

        posts = Post.objects.filter(id=122112291888818218)
        for i in range(1, int(user_profile.unlocked) + 1):
            posts |= Post.objects.filter(title=i)
            print(posts)

        ordered = []
        for post in posts:
            ordered.append(post)
        ordered = sorted(ordered, key=lambda i: int(i.title))

        context = {"user": user, "posts": ordered}
        return render(request, "users/profile.html", context)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("loginn")
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", context={"form": form})
