from django.urls import path 
from .views import * 


urlpatterns = [
    path('', index, name='index'),
    path('order/create-buy/', create_buy_view, name='create-buy'),
    path('order/create-sell/', create_sell_view, name='create-sell'),
    path('order/create-sell2/', create_sell2_view, name='create-sell2'),
    path('order/buy/<guid>/', buy_detail_view, name='buy-detail'),
    path('order/sell/<guid>/', sell_detail_view, name='sell-detail'),
    path('order/check-buy-order/<guid>/', check_buy_order, name='check-buy'),
    path('order/check-buy-confirm/<guid>/', check_buy_confirm, name='check-buy-confirm'),
    path('order/buy-success', buy_success_view, name='buy-success'),
    path('order/buy-confirm-success', buy_admin_confirm_success_view, name='buy-confirm-success'),
]
