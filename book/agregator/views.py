from django.shortcuts import render
from django.core.cache import cache
from django.views.generic import View, TemplateView
from django.http import JsonResponse

from .mixins import CustomerMixin
from favorite.service import get_list_name_book, recalculate_basket
from .agregator_book import Agregator
from .forms import SearchForm
from favorite.models import BasketItem


class BookView(TemplateView, CustomerMixin):
    template_name = 'agregator/result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = self.get_context_data(**kwargs)
        context['customer'] = self.customer
        context['basket'] = self.basket
        context['basket_list_name_book'] = get_list_name_book(self.basket)
        if cache.get(search):
            context['form'] = SearchForm()
            context['data'] = cache.get(search)
            return self.render_to_response(context)
        else:
            agregator = Agregator(str(search))
            data = agregator.main()
            context['form'] = SearchForm()
            context['data'] = data
            cache.set(search, data, timeout=60*10)
            return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        img = request.POST.get('img')
        book = request.POST.get('book')
        author = request.POST.get('author')
        price = request.POST.get('price')
        link = request.POST.get('link')
        source = request.POST.get('source')

        if self.basket.f_basket_item.filter(img=img, book=book, author=author, price=price, link=link).exists():
            book = self.basket.f_basket_item.filter(
            img=img, book=book, author=author, price=price, link=link).first()
            self.basket.books.remove(book)
            book.delete()
            recalculate_basket(self.basket)
            self.basket.save()
            return JsonResponse({'success': False})

        basket_item = BasketItem.objects.create(
            owner=self.customer,
            basket=self.basket,
            img=img,
            book=book,
            author=author,
            price=price,
            link=link,
            source=source,
        )
        self.basket.books.add(basket_item)
        recalculate_basket(self.basket)
        self.basket.save() 
        return JsonResponse({'success': True})


class HomeView(CustomerMixin):

    def get(self, request, *args, **kwargs):
        context = {}
        if not request.session.exists(request.session.session_key):
            request.session.create()     
        if request.user.is_authenticated:
            context['email'] = request.user.email 
        context['form'] = SearchForm()
        context['customer'] = self.customer
        context['basket'] = self.basket
        return render(request, 'agregator/index.html', context)

