from django.db import models
from dataclasses import dataclass


# Create your models here.
class User(models.Model):
    telegram_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=255, null=True)
    full_name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'User: {self.telegram_id}'

    class Meta:
        db_table = 'users'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_info = models.JSONField()
    amount = models.DecimalField(max_digits=16, decimal_places=4)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return f'Order: {self.id}. User: {self.user.telegram_id}'

    class Meta:
        db_table = 'orders'


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pay_address = models.CharField(max_length=255)
    currency = models.CharField(max_length=16)
    usd_amount = models.DecimalField(max_digits=16, decimal_places=4)
    pay_amount = models.DecimalField(max_digits=16, decimal_places=8)
    paid = models.BooleanField(default=False)
    payment_id = models.IntegerField(null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'


# @dataclass
class PaidContent(models.Model):
    paid_content_id = models.AutoField(primary_key=True)
    content_name = models.CharField(max_length=100)
    url = models.URLField()
    content_HTML = models.TextField()

    def __str__(self):
        return self.content_name

    class Meta:
        db_table = 'paid_content'
