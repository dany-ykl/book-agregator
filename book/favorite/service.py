from re import S
from signal import raise_signal
from .models import Basket
from django.db import models

def recalculate_basket(basket: Basket):
    basket.total_books = basket.books.count()
    basket_data = basket.books.aggregate(models.Sum('price'))
    if basket_data['price__sum']:
        basket.final_price = basket_data['price__sum']
    else:
        basket.final_price = 0
    basket.save()

def get_list_name_book(basket: Basket):
        name_book = []
        image = []
        for i in basket.f_basket_item.values('book'):
            for key, book in i.items():
                name_book.append(book)
        for i in basket.f_basket_item.values('img'):
            for key, book in i.items():
                image.append(book)


        return list(map(lambda x,y:x+y, name_book, image))