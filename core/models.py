from django.db import models
from django.utils import timezone 
import uuid 
import random 
import string 


def generate_random_string(length=30):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string 


class CommonAbstract(models.Model):
    created_at = models.DateTimeField(editable=False, verbose_name='Thời điểm tạo')
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='Thời điểm cập nhật')


    class Meta:
        ordering = ('-created_at',)
        abstract = True 


    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        super(CommonAbstract, self).save(*args, **kwargs)


class SEOAbstract(models.Model):
    meta_title = models.TextField(null=True, blank=True, verbose_name='SEO Title')
    meta_desc = models.TextField(null=True, blank=True, verbose_name='SEO Description')
    meta_keywords = models.TextField(null=True, blank=True, verbose_name='SEO Keywords')


    class Meta:
        abstract = True 

    
class CryptoType(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Tên Coin')
    alias = models.CharField(max_length=255, null=True, blank=True, verbose_name='Slug')
    symbol = models.CharField(max_length=7, verbose_name='Ký hiệu')


    class Meta:
        verbose_name = 'Loại tiền điện tử'
        verbose_name_plural = 'Loại tiền điện tử'
        db_table = 'crypto_type'

    def __str__(self):
        return f"{self.symbol} - {self.name if self.name else ''}"
    

class CryptoPrice(CommonAbstract):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False,
        verbose_name='id', help_text='Khóa chính bảng giá tiền điện tử')
    coin = models.ForeignKey(CryptoType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Coin')
    price = models.DecimalField(max_digits=20, decimal_places=8, verbose_name='Giá')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Thời điểm lấy giá')


    class Meta:
        ordering = ('-timestamp',)
        verbose_name = 'Giá tiền điện tử'
        verbose_name_plural = 'Giá tiền điện tử'
        db_table = 'crypto_price'
    

    def __str__(self):
        return f"{self.coin.symbol if self.coin else self.id} - {self.price}" 
    

class BuyTransaction(CommonAbstract):
    TRANSACTIOn_STATUS = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Time Up', 'Time Up')
    )

    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    guid = models.UUIDField(default=uuid.uuid4, null=True, blank=True, verbose_name='Mã giao dịch mua')
    transaction_type = models.CharField(max_length=15, default='buy', verbose_name='Lọai giao dịch')
    amount = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True, verbose_name='Tên coin')
    coin_name = models.CharField(max_length=7, null=True, blank=True, verbose_name='Coin')
    coin = models.ForeignKey(CryptoType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Coin')
    price_transfer = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True, verbose_name='Giá chuyển đổi')
    currency = models.CharField(max_length=7, default='VND', verbose_name='Tiền tệ')
    count_down = models.IntegerField(default=600, verbose_name='Thời gian giao dịch hiệu lực (seconds)')

    user_email = models.EmailField(max_length=255, null=True, blank=True, verbose_name='Email người mua')
    wallet_address = models.CharField(max_length=42, null=True, blank=True, verbose_name='Địa chỉ ví mua')
    blockchain_net = models.CharField(max_length=255, default='BNB Smart Chain (BEP20)', verbose_name='Mạng lưới blockchain')

    fee = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True, verbose_name='Phí giao dịch')
    remain = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True, verbose_name='Số coin thực nhận')

    description_bank = models.CharField(max_length=50, null=True, blank=True, verbose_name='Nội dung chuyển khoản')
    status = models.CharField(max_length=20, default='Pending', verbose_name='Trạng thái giao dịch')

    admin_done = models.BooleanField(default=False, verbose_name='Xác nhận của Admin')


    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Giao dịch mua'
        verbose_name_plural = 'Giao dịch mua'
        db_table = 'buy_transactions'
    

    def __str__(self):
        return f"{self.id} - {self.guid} - Admin: {self.admin_done}"


    def save(self, *args, **kwargs):
        if not self.description_bank:
            self.description_bank = generate_random_string()

        super(BuyTransaction, self).save(*args, **kwargs)


class SellTransaction(CommonAbstract):
    TRANSACTIOn_STATUS = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Time Up', 'Time Up')
    )

    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')

    guid = models.UUIDField(default=uuid.uuid4, null=True, blank=True, verbose_name='Mã giao dịch bán')
    transaction_type = models.CharField(max_length=15, default='sell', verbose_name='Loại giao dịch')
    
    amount = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True, verbose_name='Số lượng bán')
    coin_name = models.CharField(max_length=7, null=True, blank=True, verbose_name='Tên coin')
    coin = models.ForeignKey(CryptoType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Coin')
    price_transfer = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True, verbose_name='Giá chuyển đổi')
    currency = models.CharField(max_length=7, default='VND', verbose_name='Loại tiền tệ chuyển đổi')
    count_down = models.IntegerField(default=600, verbose_name='Thời hạn giao dịch (giây)')

    user_email = models.EmailField(max_length=255, null=True, blank=True, verbose_name='Email người bán')
    blockchain_net = models.CharField(max_length=255, default='BNB Smart Chain (BEP20)', verbose_name='Mạng lưới giao dịch')

    bank_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Tên ngân hàng người bán')
    bank_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='Số tài khoản')
    bank_username = models.CharField(max_length=255, null=True, blank=True, verbose_name='Tên tài khoản')

    wallet_address_in = models.CharField(max_length=42, default='0x80c763ce49c01c6df8425ce8bbff5e4758a422ed', verbose_name='Địa chỉ ví nhận')

    fee = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True, verbose_name='Phí')
    remain = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True, verbose_name='Số tiền thực nhận')

    status = models.CharField(max_length=20, default='Pending', verbose_name='Trạng thái giao dịch')

    admin_done = models.BooleanField(default=False, verbose_name='Admin xác nhận')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Giao dịch bán'
        verbose_name_plural = 'Giao dịch bán'
        db_table = 'sell_transactions'
    
    def __str__(self):
        return f"{self.id} - {self.guid} - Admin: {self.admin_done}"


class TransactionHistory(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    debit_amount = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True, verbose_name='Số tiền')
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nội dung chuyển khoản')


    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Lịch sử giao dịch'
        verbose_name_plural = 'Lịch sử giao dịch'
        db_table = 'trans_history'


    def __str__(self):
        return f"{self.id} - {self.description}" 
    

