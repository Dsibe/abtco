from django.shortcuts import render, redirect
from .forms import *
import datetime
from django.http import HttpResponse
from main.views import *
from users.views import *
from django.contrib.auth import views as auth_views
from users.models import *

from os import environ
from users.models import *

dates = []

def psy_finance(request):
    return render(request, r'main/psy_finance.html')


def hedge_fund(request):
    return render(request, r'main/hedge-fund.html')


def departments(request):
    return render(request, r'main/departments.html')


def main(request):
    envir = environ
    global dates

    def add_unlocked(user):
        if int(user.unlocked) < 15:
            if int(user.unlocked) <= 2:
                unlocked = int(user.unlocked) + 1
                user.unlocked = unlocked
                user.save()

            elif int(user.unlocked) >= 3:
                if user.ppaid == True:
                    unlocked = int(user.unlocked) + 1
                    user.unlocked = unlocked
                    user.save()

    day = datetime.datetime.today().weekday()
    if day in [0, 3]:
        date = str(datetime.datetime.now())[:10]
        dates = Dates.objects.filter(dates=date)

        if not dates:
            Dates.objects.create(dates=date)
            for user in Profile.objects.all():
                add_unlocked(user)

    return render(request, r'main/main.html', context={'env': envir})


def ud(request):
    return HttpResponse(
        "<h1 style='text-align: center; font-family: arial; color: #21409A;'>Under Construction</h1>"
    )


def developing(request):
    return render(request, r'main/developing.html')
    # return redirect('http://www.4organizer.com')


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
            send_mail(f'New contact-us message from {email}, name: {name}',
                      message, 'abtcous2014@gmail.com',
                      ['abt.company@aol.com', 'darik.pc@gmail.com'])
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
    body = """
Онлайн-школа «ABTco-Trading School»

Программа обучения:

наш курс обучения состоит из 15 уроков,
из которых первые три вы получаете АБСОЛЮТНО бесплатно.

Изучив три урока, вы сможете понять нравится ли вам учебный материал,
стиль подачи, интересно ли изучение полного курса.

Если все нравится, от вас потребуется только оплатить оставшиеся 12 уроков.

Сделать это вы сможете с помощью онлайн-платежа прямо на нашем сайте.

Процесс оплаты не займет у вас много времени, сервис организован очень
удобно, является полностью безопасным, к оплате принимаются любые карты,

нет комиссий.
Цена нашего курса очень демократична и в несколько раз дешевле

аналогичных курсов обучения, предлагаемых на рынке.

Почему дешевле, вы узнаете из первого урока.

Если вы уже интересовались подобными курсами обучения, то порядок цен вам скорее всего знаком и вы можете сами сравнить, насколько цена нашего курса доступнее для всех.

Таким образом, у вас есть возможность попробовать отличный и
качественный продукт за доступные деньги.

Обучение трейдингу интересно многим, но очень часто стоимость курса
становится препятствием для желающих.

С нами вы ничем не рискуете: вы получаете возможность попробовать, понять для себя интересно ли вам данное направление деятельности, с вами остаются знания, вы выходите на новый уровень развития и все это за символическую цену!



Для записи доступны три группы:
1. Пн — Чт ( идет набор)
2. Вт — Пт ( интенсивное заполнение, но еще есть места)
3. Ср — Сб (места заканчиваются)
Для записи в школу необходимо заполнить форму и выбрать удобные для занятий дни.

За 15 уроков вы получите все знания,
необходимые для начала торговли на реальном(не демо!!!) счете.

От вас не потребуется никаких предварительных знаний об этом предмете. Все основные понятия, правила и терминология будут изложены в простой и доступной форме.

После изучения этого курса, вы получите достаточный объем знаний, который позволит вам понимать, как работает рынок ценных бумаг, а также все причины, которые влияют на его поведение.

Наш курс будет интересен для очень широкой аудитории людей: молодых, юных, старшего возраста, для тех, кто хотел бы попробовать себя в торговле и инвестировании на рынке акций и других ценных бумаг, но не знал как или боялся начать.
Доступ к первым трем бесплатным урокам вы получите после заполнения формы.

Во время обучения мы рассмотрим следующие темы:
Биржа - что это такое и как это работает. Ресурсы для поиска информации.
Акции и их особенности, что такое отчетность и как это использовать, фьючерсы, фонды, объемы и спред. Формула формирования безопасной позиции или как уберечь себя от убытков. Друзья среди акций - зачем они трейдеру и что с ними делать. Умение читать книгу - заказов и ленту - один из важнейших навыков и как это может спасти трейдера. Основы торговли - саппорт и сопротивление, как с ними работать. Владельцы компаний - как с ними дружить и что они могут нам сообщить. Магия чисел и как использовать ее себе во благо. Как найти направление движения акций и кто нам в этом поможет. Делаем ранний правильный прогноз - как это работает.
И это далеко не полный список наших тем!

После оплаты вы получите доступ к полному курсу по расписанию,
согласно выбранной вами группы.

Стоимость полного курса составляет — $199.99
Для записи на групповой курс нажмите на кнопку ниже.

Доступны новые опции:
<strong style="color: #F32A2E">Индивидуальное VIP обучение — $500.00</strong>
<strong style="color: #F32A2E">Обучение с ментором и оплата из ЗАРАБОТАННЫХ средств — $1995.95</strong>

Дополнительная информацию или <strong style="color: #F32A2E">запись по запросу через email:</strong> <a href="mailto:abt.company@aol.com">abt.company@aol.com</a>"""
    return render(request, r'main/trading_ru_g.html', context={'body': body})


def trading_ua_g(request):
    return render(request, r'main/trading_ua_g.html')


def business(request):
    return render(request, 'main/business.html')
