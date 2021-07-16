from django.urls import path, includeurlpatterns = [
    path('', include('shop.urls', namespace='shop', app_namespace='shop')),
]
