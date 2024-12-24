from django.contrib import admin
from .models import * 


@admin.register(CryptoType)
class CryptoTypeAdmin(admin.ModelAdmin):
    search_fields = ['name', 'alias', 'symbol']
    list_display = ['name', 'symbol', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    readonly_fields = ['created_at',]


@admin.register(CryptoPrice)
class CryptoPriceAdmin(admin.ModelAdmin):
    search_fields = ['price', 'id']
    list_display = ['coin', 'price', 'timestamp']
    list_filter = ['created_at', 'updated_at', 'coin']
    readonly_fields = ['created_at', 'timestamp']


@admin.register(BuyTransaction)
class BuyTransactionAdmin(admin.ModelAdmin):
    search_fields = ['guid', 'coin', 'coin_name', 'user_email', 'wallet_address',]
    list_display = ['description_bank', 'price_transfer', 'user_email', 'status', 'admin_done']
    list_filter = ['coin', 'user_email', 'wallet_address', 'status', 'admin_done']
    readonly_fields = ['created_at',]


@admin.register(SellTransaction)
class SellTransactionAdmin(admin.ModelAdmin):
    search_fields = ['guid', 'coin', 'coin_name', 'user_email',]
    list_display = ['price_transfer', 'user_email', 'status', 'admin_done']
    list_filter = ['coin', 'user_email', 'status', 'admin_done']
    readonly_fields = ['created_at',]


@admin.register(TransactionHistory)
class TransactionHistoryAdmin(admin.ModelAdmin):
    search_fields = ['debit_amount', 'description']
    list_display = ['debit_amount', 'description']
    list_filter = ['created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at', 'debit_amount', 'description']
