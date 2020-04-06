from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import Context, Template
from django.contrib.auth.models import User
from .models import *
from .forms import *
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received

from django.core.mail import send_mail

from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm


def thirdlesson(request):
    return redirect("process_payment")


def process_payment(request, course):

    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=request.user)
    print(type(profile))

    host = request.get_host()

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "49.99",
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

    # ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        print("Received payment")

        profile = ipn_obj.custom
        user = User.objects.get(username=profile)
        profile = Profile.objects.get(user=user)
        print()
        print(type(profile))
        print()
        # user = ipn_obj.custom[0]

        profile.ppaid = True
        profile.save()
        print("save")

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
        print("Failed")


valid_ipn_received.connect(show_me_the_money)

invalid_ipn_received.connect(show_me_the_money)


@login_required
def post_detail(request, slug):
    post = get_object_or_404(Post, slug__iexact=slug)
    body = post.body
    body = body.replace("<r>", '<span style="color: red;">')
    body = body.replace("</r>", "</span>")
    body = body.replace("<g>", '<span style="color: #28ed12;">')
    body = body.replace("</g>", "</span>")
    body = body.replace("<b>", '<span style="color: #21409a;">')
    body = body.replace("</b>", "</span>")
    body = body.replace("<r", '<span style="color: red;">')
    body = body.replace("r>", "</span>")
    body = body.replace("<g", '<span style="color: #28ed12;">')
    body = body.replace("g>", "</span>")
    body = body.replace("<b", '<span style="color: #21409a;">')
    body = body.replace("b>", "</span>")
    body = body.replace("<R>", '<span style="color: red;">')
    body = body.replace("</R>", "</span>")
    body = body.replace("<G>", '<span style="color: #28ed12;">')
    body = body.replace("</G>", "</span>")
    body = body.replace("<B>", '<span style="color: #21409a;">')
    body = body.replace("</B>", "</span>")
    body = body.replace("<R", '<span style="color: red;">')
    body = body.replace("R>", "</span>")
    body = body.replace("<G", '<span style="color: #28ed12;">')
    body = body.replace("G>", "</span>")
    body = body.replace("<B", '<span style="color: #21409a;">')
    body = body.replace("B>", "</span>")

    # body = body.replace('<a', '<a href="">')
    # body = body.replace('a>', '</a>')
    #
    # to_find = True
    # while to_find:
    #     if body.find('<a href="">') != -1:
    #         link = body[body.find('<a href="">'):body.find('</a>')]
    #         body = body.replace('<a href="">', f'<a href="{link}">')
    #     else:
    #         to_find = False

    post.body = body
    context = {"post": post}
    if post.title == "3":
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user=request.user)
        print(type(profile))

        host = request.get_host()

        paypal_dict = {
            "business":
            settings.PAYPAL_RECEIVER_EMAIL,
            "amount":
            "49.95",
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
        print(user_profile.unlocked)
        for i in range(1, int(user_profile.unlocked) + 1):
            posts |= Post.objects.filter(title=i)
            print(posts)
        posts = posts.order_by('title')
        context = {"user": user, "posts": posts}
        return render(request, "users/profile.html", context)


# def login(request):
#       return render(request, 'users/login-fb.html')


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("loginn")
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", context={"form": form})
