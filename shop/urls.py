from django.contrib.auth import views as auth_views
from django.urls import path, include
from shop.views import *
from sellapp import views as sell_views

app_name = 'shop'

urlpatterns = [
    path('update-profile', update_profile, name='update_profile'),
    path('unban-machine/<int:machine_id>/', sell_views.unban_machine),
    path('ban-machine/<int:machine_id>/', sell_views.ban_machine),
    path('view-machines/<int:license_id>',
         sell_views.view_machines,
         name='view_machines'),
    path('decrypt-code-with-license',
         sell_views.decrypt_code_with_license,
         name='decrypt-code-with-license'),
    path('license-check/<path:args>',
         sell_views.license_check,
         name='license-check'),
    path('', main, name='shop_main'),
    path('contact-us', contact_us, name='shop_contact-us'),
    path('register', register, name='shop_register'),
    path('login-or-signup', login_or_signup),
    path('profile', profile, name='profile'),
    path('login',
         auth_views.LoginView.as_view(template_name='shop/login.html',
                                      extra_context={'next': 'profile'}),
         name='shop-login'),
    path('logout',
         auth_views.LogoutView.as_view(template_name='shop/logout.html'),
         name='shop_logout'),
    path('app/<str:name_id>', show_app),
    path(
        'buy-license/<str:app_name_id>/<str:pricing_id>/<int:period>/<int:max_machines_amount>/',
        buy_license),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-done/', payment_done, name='payment_done'),
    path('payment-cancelled/', payment_canceled, name='payment_cancelled'),
]
