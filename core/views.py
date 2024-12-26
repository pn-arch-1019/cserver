from django.shortcuts import render, redirect 
from django.urls import reverse 
from .models import * 
from django.http import JsonResponse 
from django.utils import timezone 
import requests 


def robots_txt(request):
    content = "User-agent: *\nDisallow: /admin/\nSitemap: https://coinbotc.net/sitemap.xml"
    return HttpResponse(content, content_type='text/plain')


def index(request):
    coins = CryptoType.objects.all()
    context = {}
    for coin in coins:
        context[coin.symbol] = CryptoPrice.objects.filter(coin=coin).order_by('-timestamp').first()
    # print(context)
    return render(request, 'index.html', context)


def create_buy_view(request):
    if request.method == 'POST':
        amount = request.POST.get('buy-amount')
        coin_name = request.POST.get('buy-option')
        price_transfer = request.POST.get('buy-transfer')
        buy_currency = request.POST.get('buy-currency')
        user_email = request.POST.get('email')
        wallet_address = request.POST.get('wallet-address')

        coin = CryptoType.objects.get(symbol=coin_name)
        # print(coin_name)

        buy_transaction = BuyTransaction.objects.create(
            amount=float(amount),
            coin_name=coin_name,
            coin=coin,
            price_transfer=float(price_transfer),
            user_email=user_email,
            wallet_address=wallet_address,
            fee=float(amount)*0.000005,
            remain=float(amount)*0.999995,
        )

        return redirect(reverse('buy-detail', kwargs={'guid': buy_transaction.guid}))


    buyAmount = request.GET.get('buy-amount')
    buyOption = request.GET.get('buy-option')
    buyTransfer = request.GET.get('buy-transfer')
    buyCurrency = request.GET.get('buy-currency')

    print(buyAmount)
    print(buyOption)
    print(buyTransfer)
    print(buyCurrency)
    context = {}
    context['buyAmount'] = buyAmount
    context['buyOption'] = buyOption
    context['buyTransfer'] = buyTransfer    
    context['buyCurrency'] = buyCurrency
    context['fee'] = float(buyAmount) * 0.000005
    context['remain'] = float(buyAmount) * 0.999995

    return render(request, 'create-buy.html', context)


def buy_detail_view(request, guid):
    try:
        buy_trans = BuyTransaction.objects.get(guid=guid)
    except BuyTransaction.DoesNotExits():
        return redirect('index')

    BANK_NAME = "970422"
    BANK_ACCOUNT = "4010192949848"
    ACCOUNT_NAME = r"NGUYEN%20VAN%20LONG"
    desc = buy_trans.description_bank 
    amount = int(buy_trans.price_transfer) 
    print(f"AMOUNT: {amount}")


    qr_img_url = f"https://img.vietqr.io/image/{BANK_NAME}-{BANK_ACCOUNT}-compact2.png?amount={amount}&addInfo={desc}&accountName={ACCOUNT_NAME}"
    print(qr_img_url)
    context  = {}
    context['buy_trans'] = buy_trans
    context['qr_img_url'] = qr_img_url 
    return render(request, 'buy-detail.html', context)


def create_sell_view(request):
    sellAmount = request.GET.get('sell-amount')
    sellOption = request.GET.get('sell-option')
    sellTransfer = request.GET.get('sell-transfer')
    sellCurrency = request.GET.get('sell-currency')

    print(sellAmount)
    print(sellOption)
    print(sellTransfer)
    print(sellCurrency)

    context = {}
    context['sellAmount'] = sellAmount
    context['sellOption'] = sellOption
    context['sellTransfer'] = sellTransfer
    context['sellCurrency'] = sellCurrency 
    context['fee'] = 10000
    context['remain'] = float(sellTransfer) - 10000

    return render(request, 'create-sell.html', context)


def create_sell2_view(request):
    if request.method == 'POST':
        amount = request.POST.get('sell-amount')
        coin_name = request.POST.get('sell-option')
        price_transfer = request.POST.get('sell-transfer')
        currency = request.POST.get('sell-currency')
        user_email = request.POST.get('user-email')
        bank_name = request.POST.get('bank_name')
        bank_number = request.POST.get('bank_number')
        bank_username = request.POST.get('bank_username')

        fee = 10000
        remain = float(price_transfer) - 10000 

        coin = CryptoType.objects.get(symbol=coin_name)
        # print(coin_name)

        sell_transaction = SellTransaction.objects.create(
            amount=float(amount),
            coin_name=coin_name,
            coin=coin,
            price_transfer=int(price_transfer),
            user_email=user_email,
            fee=10000,
            remain=remain,
            bank_name=bank_name,
            bank_number=bank_number,
            bank_username=bank_username
        )

        return redirect(reverse('sell-detail', kwargs={'guid': sell_transaction.guid}))



    sellAmount   = request.GET.get('sell-amount')
    sellOption = request.GET.get('sell-option')
    sellTransfer = request.GET.get('sell-transfer')
    sellCurrency = request.GET.get('sell-currency')
    user_email = request.GET.get('email')
    blockchain_net = request.GET.get('blockchain-net')

    print(sellAmount)
    print(sellOption)
    print(sellTransfer)
    print(sellCurrency)
    print(user_email)
    print(blockchain_net)

    context = {}
    context['sellAmount'] = sellAmount
    context['sellOption'] = sellOption
    context['sellTransfer'] = sellTransfer
    context['sellCurrency'] = sellCurrency
    context['user_email'] = user_email
    context['blockchain_net'] = blockchain_net
    context['fee'] = 10000 
    print(context)
    context['remain'] = float(sellTransfer) - 10000

    return render(request, 'create-sell2.html', context)


def sell_detail_view(request, guid):
    try:
        sell_trans = SellTransaction.objects.get(guid=guid)
    except SellTransaction.DoesNotExits():
        return redirect('index')
    context = {}
    context['sell_trans'] = sell_trans 
    return render(request, 'sell-detail.html', context)


def check_buy_order(request, guid):
    try:
        buy_trans = BuyTransaction.objects.get(guid=guid)
    except BuyTransaction.DoesNotExits():
        return JsonResponse({
            'flag': False,
        })

    today = timezone.now().date()

    lsgd_today = TransactionHistory.objects.filter(created_at__date=today)
    
    print(lsgd_today)

    for lsgd in lsgd_today:
        print(buy_trans.description_bank)
        print(lsgd.description)
        print(int(buy_trans.price_transfer))
        print(int(lsgd.debit_amount))
        if buy_trans.description_bank in lsgd.description.replace(' ', '') and int(buy_trans.price_transfer) == int(lsgd.debit_amount):
            buy_trans.status = 'Completed'
            buy_trans.save()

            return JsonResponse({
                'flag': True
            })

    return JsonResponse({
        'flag': False
    })
    

def check_buy_confirm(request, guid):
    try:
        buy_trans = BuyTransaction.objects.get(guid=guid)
    except BuyTransaction.DoesNotExist():
        return JsonResponse({
            'flag': False,
        })
    if buy_trans.admin_done:
        return JsonResponse({
            'flag': True 
        })
    return JsonResponse({
        'flag': False 
    })


def buy_success_view(request):
    buy_guid = request.GET.get('tran-guid')
    # print(buy_guid)

    try:
        buy_trans = BuyTransaction.objects.get(guid=buy_guid)
    except BuyTransaction.DoesNotExist():
        return redirect('index')

    return render(request, 'buy-success.html', {'buy_trans': buy_trans})


def buy_admin_confirm_success_view(request):
    return render(request, 'buy-confirm-success.html')


import hashlib
import hmac
import json
import urllib
import urllib.parse
import urllib.request
import random
import requests
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect


def hmacsha512(key, data):
    byteKey = key.encode('utf-8')
    byteData = data.encode('utf-8')
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

n = random.randint(10**11, 10**12 - 1)
n_str = str(n)
while len(n_str) < 12:
    n_str = '0' + n_str


