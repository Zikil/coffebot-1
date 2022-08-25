from django.urls import path

from .views import *

urlpatterns = [
    path('', create_buying, name='create-buying'),
    path('create-order-form/', create_order_form, name='create-order-form'),
    path('order/<pk>/', detail_order, name='detail-order'),
    path('buying/<pk>/', detail_buying, name='detail-buying'),
    path('order/<pk>/update/', update_order, name='update-order'),
    path('order/<pk>/delete/', delete_order, name='delete-order'),
    path('customer/', get_customer, name='get-customer'),
    path('<pk>/customer', create_buy_customer, name='create-buy-customer'),
    path('<pk>/', create_buy_order, name='create-buy-order'),




    
    # path('all/', paste_list, name='paste_list_url'),
]
