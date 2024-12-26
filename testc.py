import requests 

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
        "payTypes": ["BANK"],
        "publisherType": None
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        prices = response.json()
        print(prices['data'][0]['adv']['price'])
        print(prices['data'][1]['adv']['price'])
        print(prices['data'][2]['adv']['price'])
        print(prices['data'][3]['adv']['price'])
        print(prices['data'][4]['adv']['price'])
        print(prices['data'][5]['adv']['price'])
        print(prices['data'][6]['adv']['price'])
        print(prices['data'][7]['adv']['price'])
        print(prices['data'][8]['adv']['price'])
        print(prices['data'][9]['adv']['price'])
        if prices['data']:
            last_ad = prices['data'][0]
            print(f"Giá USDT cuối cùng: {last_ad['adv']['price']}, Số lượng giao dịch còn lại: {last_ad['adv']['surplusAmount']}") 
            price = last_ad['adv']['price'] if last_ad['adv']['price'] else None 
            return price 
        else:
            print("Không có dữ liệu giá USDT.")
            return None 

    else:
        print(f"Error: {response.status_code}")
        return None 
    

get_binance_p2p_usdt_price()