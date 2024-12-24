from django.conf import settings 
import requests 
from core.models import * 
from datetime import datetime 
from decouple import config 


def get_binance_p2p_usdt_price():
    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    data = {
        "asset": "USDT",
        "fiat": "VND",  # có thể thay đổi nếu muốn lấy giá bằng tiền tệ khác
        "tradeType": "BUY",
        "transAmount": "",  # Số lượng USDT muốn mua
        "page": 1,
        "rows": 10,
        "payTypes": [],
        "publisherType": None
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        prices = response.json()
        if prices['data']:
            last_ad = prices['data'][-1]
            print(f"Giá USDT cuối cùng: {last_ad['adv']['price']}, Số lượng giao dịch còn lại: {last_ad['adv']['surplusAmount']}") 
            price = last_ad['adv']['price'] if last_ad['adv']['price'] else None 
            return price 
        else:
            print("Không có dữ liệu giá USDT.")
            return None 

    else:
        print(f"Error: {response.status_code}")
        return None 


def get_binance_p2p_bnb_price():
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    data = {
        "asset": "BNB",  # Thay đổi từ USDT sang BNB
        "fiat": "VND",   # có thể thay đổi sang loại tiền khác nếu muốn
        "tradeType": "BUY",  # Hoặc "SELL" nếu muốn xem giá bán
        "transAmount": "",  # Số lượng BNB muốn mua (có thể để trống)
        "page": 1,
        "rows": 10,
        "payTypes": [],
        "publisherType": None
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        prices = response.json()
        if prices['data']:
            last_ad = prices['data'][-1]
            price = last_ad['adv']['price']
            trade_amount = last_ad['adv']['surplusAmount']
            print(f"Giá BNB cuối cùng: {price}, Số lượng giao dịch còn lại: {trade_amount}")
            return price
        else:
            print("Không có dữ liệu giá BNB.")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None


def get_binance_p2p_price(asset):
    """
    Lấy giá P2P của tài sản (USDT, BTC, ETH,...) từ Binance.
    """
    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    data = {
        "asset": asset,  # Tên tài sản: USDT, BTC, ETH,...
        "fiat": "VND",   # Có thể thay đổi nếu muốn lấy giá bằng tiền tệ khác
        "tradeType": "BUY",
        "transAmount": "",  # Số lượng tài sản muốn mua
        "page": 1,
        "rows": 10,
        "payTypes": [],
        "publisherType": None
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        prices = response.json()
        if prices['data']:
            last_ad = prices['data'][0]
            print(f"Giá {asset} cuối cùng: {last_ad['adv']['price']}, Số lượng giao dịch còn lại: {last_ad['adv']['surplusAmount']}")
            price = last_ad['adv']['price'] if last_ad['adv']['price'] else None
            return price
        else:
            print(f"Không có dữ liệu giá {asset}.")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None
    

def update_coint_price_vnd():
    print("-----------------START PRICE-----------------------")
    try:
        coins = CryptoType.objects.all()
        usdt_price = get_binance_p2p_usdt_price()
        bnb_price = get_binance_p2p_bnb_price()
        btc_price = get_binance_p2p_price('BTC')
        eth_price = get_binance_p2p_price('ETH')

        for coin in coins:
            if coin.symbol == 'BTC':
                if btc_price is not None:
                    try:
                        btc = CryptoPrice.objects.create(
                            coin=coin,
                            price=float(btc_price)
                        )
                        print("Save btc ok!")
                    except:
                        pass 
            elif coin.symbol == 'ETH':
                if eth_price is not None:
                    try:
                        eth = CryptoPrice.objects.create(
                            coin=coin,
                            price=float(eth_price)
                        )
                        print("Save eth ok!")
                    except:
                        pass
            elif coin.symbol == 'USDT':
                if usdt_price is not None:
                    try:
                        usdt = CryptoPrice.objects.create(
                            coin=coin,
                            price=float(usdt_price)
                        )
                        print("Save usdt ok!")
                    except:
                        pass 
            elif coin.symbol == 'BNB':
                if bnb_price is not None:
                    try:
                        bnb = CryptoPrice.objects.create(
                            coin=coin,
                            price=float(bnb_price)
                        )
                        print("Save bnb ok!")
                    except:
                        pass 

    except Exception as e:
        print(f"Error: {str(e)}")
    print("-----------------END PRICE-----------------------")


from mbbank2.main import MBBank 
import threading 
from datetime import datetime 
from django.utils import timezone 


global_obj = None 


def update_global_obj():
    global global_obj 
    USERNAME_BANK = config('USERNAME_BANK')
    PASSWORD = config('PASSWORD')
    global_obj = MBBank(username=USERNAME_BANK, password=PASSWORD)
    
    print("Updated global_obj")

    # Đặt lại Timer để cập nhật mỗi tiếng
    threading.Timer(3600, update_global_obj).start() 


update_global_obj()


def get_trans_new():
    global global_obj 
    ACCOUNT_NO = config('ACCOUNT_NO')

    lsgd = global_obj.getTransactionAccountHistory(
        accountNo=ACCOUNT_NO,
        from_date=datetime.now(),
        to_date=datetime.now()
    )

    lsgd_list = lsgd['transactionHistoryList'] 
    print(lsgd_list)
    today = timezone.now().date()
    lsgd_today = TransactionHistory.objects.filter(created_at__date=today)
    for item in lsgd_list: 
        credit_amount = item['debitAmount'] if int(item['debitAmount']) != 0 else item['creditAmount'] 
        desc = str(item['addDescription']).replace(' ', '')

        record_exists = lsgd_today.filter(
            debit_amount=float(credit_amount),
            description=desc
        ).exists()
        if not record_exists:
            new_lsgd = TransactionHistory.objects.create(
                debit_amount=credit_amount,
                description=desc
            )
            print("Save new!") 
        else:
            print("No")


