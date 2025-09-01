from django.urls import path
from core.views import home, menu, tracking, reservation, contact, cart_detail, cart_add, cart_remove, cart_increase, cart_decrease

urlpatterns = [
    path('', home, name='home'),
    path('menu/', menu, name='menu'),
    path('order-track/', tracking, name='track'),
    path('reservation/', reservation, name='reservation'),
    path('contact/', contact, name='contact'),
    path('cart/', cart_detail, name='cart'),
    path('cart/add/<int:dish_id>/', cart_add, name='cart_add'),
    path('cart/remove/<int:dish_id>/', cart_remove, name='cart_remove'),
    path('cart/increase/<int:dish_id>/', cart_increase, name='cart_increase'),
    path('cart/decrease/<int:dish_id>/', cart_decrease, name='cart_decrease'),
]
