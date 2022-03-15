import json
from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.http import JsonResponse

from agregator.mixins import CustomerMixin
from favorite.models import Basket, BasketItem, Customer
from .service import recalculate_basket, get_list_name_book


class BookView(TemplateView, CustomerMixin):

    template_name = 'favorite/favorite.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notsearch'] = True
        context['customer'] = self.customer
        context['basket'] = self.basket
        context['basket_list'] = self.basket.f_basket_item.all()
        context['basket_list_name_book'] = get_list_name_book(self.basket)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        article = request.POST.get('article')
        book = BasketItem.objects.filter(article=article).first()
        print(book)
        self.basket.books.remove(book)
        book.delete()
        recalculate_basket(self.basket)
        self.basket.save()
        return JsonResponse({'success':True})
