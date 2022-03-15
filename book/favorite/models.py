import uuid

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from accounts.models import CustomUser


class Customer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    anonymos_user = models.BooleanField(default=False)
    session_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        if self.user:
            return str(self.user)
        else:
            return self.session_id

class Basket(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    books = models.ManyToManyField('BasketItem', blank=True, related_name='f_basket')
    total_books = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2)

    def __str__(self):
        return str(self.owner)

class BasketItem(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    basket = models.ForeignKey('Basket', on_delete=models.CASCADE, related_name='f_basket_item')
    img = models.CharField(max_length=200)
    book = models.CharField(max_length=300)
    author = models.CharField(max_length=300, null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    link = models.URLField(max_length=400)
    source = models.CharField(max_length=50)
    article = models.UUIDField(default=uuid.uuid4)

    def __str__(self) -> str:
        return f'{self.book}|{self.author}'