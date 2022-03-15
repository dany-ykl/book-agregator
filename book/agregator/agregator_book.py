import asyncio
import logging
import random
from types import NoneType
from xmlrpc.client import ResponseError
from  aiohttp import ClientSession
from typing import List, Dict, Union
from bs4 import BeautifulSoup
from lxml import etree
from incapsula import IncapSession

from .service import user_agent
from .ozon_env import ozon_headers

logger = logging.getLogger(__name__)

class Agregator:

    def __init__(self, search) -> None:
        self.search = search
        self.user_agent = user_agent()
        self.data = []

    async def get_html_and_class_tag(self, session:ClientSession) -> Dict:
            data = {}
            link = 'https://www.bookvoed.ru/books'
            _params = {'q':self.search}
            headers = {'user-agent':self.user_agent}
            try:
                async with session.get(link, params=_params, headers=headers) as r:
                    text = await r.text()
                    data['text'] = text
                    parser = etree.HTMLParser()
                    dom = etree.HTML(text, parser)
                    books = dom.xpath('//*[@id="books"]')
                    data["card_book"] = books[0].xpath('div[3]/div/div[1]/@class')
                    data["class_name_href"] = books[0].xpath('div[3]/div/div[1]/div[2]/div[1]/a/@class')
                    data["class_author"] = books[0].xpath('div[3]/div/div[1]/div[2]/div[2]/@class')
                    data["class_price"] = books[0].xpath('div[3]/div/div[1]/div[3]/div[1]/@class')
                    return data
            except:
                logger.error(f'get_html_and_class_tag')
                return None

    async def featch_data_bookvoed(self, session:ClientSession):
        """Часто меняет название классов!"""
        try:
            text_and_classes_tag = await self.get_html_and_class_tag(session)
            class_price = text_and_classes_tag['class_price']
            class_name_href = text_and_classes_tag['class_name_href']
            class_author = text_and_classes_tag['class_author']
            card_book = text_and_classes_tag["card_book"]
            site = 'https://www.bookvoed.ru'
            url = 'https://www.bookvoed.ru/books'
            text = text_and_classes_tag['text']
            soup = BeautifulSoup(text, 'lxml')
            books = soup.find('div', id="books")
            cart_book = books.find_all('div', class_=card_book)
            for i in cart_book[:6]:
                data_book = {}
                available = i.find('div', class_=class_price)
                if available:
                    data_book["img"] = site+i.find('img')['src']
                    data_book["book"] = i.find('a', class_=class_name_href).text.strip()
                    try:
                        data_book["author"] = i.find('div', class_=class_author).text.strip()
                    except: 
                        data_book["author"] = ''
                    try:
                        data_book["price"] = "".join(i.find('div', class_=class_price).text.split()).rstrip('₽')
                    except:
                        data_book["price"] = ''
                    data_book["link"] = i.find('a')['href']
                    data_book["available"] = True
                    data_book["source"] = "Буквоед"
                    data_book['id'] = str(random.randint(1000,10000))
                    self.data.append(data_book)
        except:
            logger.error(self.featch_data_bookvoed.__name__)
            return None
             
    async def get_price_book24(self, session:ClientSession, headers:dict, url:str) -> Union[str, None]:
        async with session.get(url, headers=headers) as r:
            text = await r.text()
            soup = BeautifulSoup(text, 'lxml')
            try:
                price = "".join(soup.find('div', class_='product-sidebar-price__main-price') \
                    .find('span').text.split()).rstrip('₽')
                return price
            except:
                return '-'

    async def featch_data_book24(self, session:ClientSession) -> None:
        try:
            site = 'https://book24.ru'
            url = 'https://book24.ru/search'
            _params = {'q':self.search}
            headers = {'User-Agent':self.user_agent}
            async with session.get(url, headers=headers, params=_params) as r:
                if r.status != 200:
                    logger.error(f"featch_data_book24:{r.status}")
                    return None
                else:
                    text = await r.text()
                    soup = BeautifulSoup(text, 'lxml')
                    books = soup.find('div', class_='catalog__product-list-holder')
                    cart_book = books.find_all('div', class_='product-list__item')
                    for book in cart_book[:6]:
                        data_book = {}
                        data_book["img"] = book.find('picture', class_='product-card__picture').find('img')['data-src']
                        data_book["book"] = book.find('a', class_='product-card__name').text 
                        try:
                            author = book.find('div', class_='author-list product-card__authors-holder')
                            data_book["author"] = author.text
                        except: 
                            data_book["author"] = ''
                        link = site+book.find('a', class_='product-card__name')['href']
                        data_book["price"] = await self.get_price_book24(session, headers, link)
                        data_book["link"] = link
                        data_book["available"] = True
                        data_book["source"] = 'Book24'
                        data_book['id'] = str(random.randint(1000,10000))
                        self.data.append(data_book)

        except:
            logger.error(self.featch_data_book24.__name__)
            return None

    async def featch_data_fkniga(self, session:ClientSession) -> None:
        try:
            site = 'https://fkniga.ru'
            link = 'https://fkniga.ru/search/'
            headers = {'User-Agent':self.user_agent}
            _params = {'q':self.search}
            async with session.get(link, headers=headers, params=_params) as r:
                if r.status != 200:
                    logger.error(f"featch_data_fkniga:{r.status}")
                    return None
                text = await r.text()
                soup = BeautifulSoup(text, 'lxml')
                catalog = soup.find('div', class_='category-cards-container js-catalog-content')
                if type(catalog) != NoneType:
                    books = catalog.find_all('div', class_='grid__item')
                    for book in books[:5]:
                        data_book = {}
                        data_book["img"] = site+book.find('img')['src']
                        data_book["book"] = book.find('a', class_='card__title').text.strip()
                        try:
                            data_book["author"] = book.find('div', class_='card__subtitle').text.replace('Автор: ','')
                        except:
                            data_book["author"] = ''
                        data_book["price"] = book.find('div', class_='price price--ruble').text
                        data_book["link"] = site+book.find('a', class_='card__title')['href']
                        data_book["available"] = True
                        data_book["source"] = 'Fkniga'
                        data_book['id'] = str(random.randint(1000,10000))
                        self.data.append(data_book)
                else:
                    logger.error(f"{self.featch_data_fkniga.__name__}:NoneType")
                    return None

        except:
           logger.error(self.featch_data_fkniga.__name__)
           return None

    async def featch_data_labirint(self, session:ClientSession) -> None:
        try:
            site = 'https://www.labirint.ru'
            link = f'https://www.labirint.ru/search/{self.search}'
            headers = {'User-Agent':self.user_agent}
            async with session.get(link, headers=headers) as r:
                if r.status != 200:
                    logger.error(f"featch_data_labirint:{r.status}")
                    return None
                text = await r.text()
                soup = BeautifulSoup(text, 'lxml')
                products = soup.find('div', class_='products-row')
                cart_product = products.find_all('div', class_='card-column')
                for i in cart_product[:6]:
                    data_book = {}
                    available = i.find('span', class_='price-val price-gray price-missing') 
                    if  available is None:
                        p = i.find('div', class_='product-cover')
                        data_book["img"] = p.find('a', class_='cover').img['data-src']
                        data_book["book"] = (i.find('div')['data-name'])
                        try:
                            data_book["author"] = i.find('div', class_='product-author').find('span').text
                        except:
                            data_book["author"] = ''
                        data_book["price"] = i.find('div')['data-price']
                        data_book["link"] = site+p.find('a', class_='cover')['href']
                        data_book["available"] = True
                        data_book["source"] = 'Labirint'
                        data_book['id'] = str(random.randint(1000,10000))
                        self.data.append(data_book)
            
        except: 
            logger.error(self.featch_data_labirint.__name__)
            return None

    async def featch_data_ozon(self) -> None:
        try:
            _params = {'text':self.search}
            site = 'https://www.ozon.ru'
            url = 'https://www.ozon.ru/category/knigi-16500'
            session = IncapSession()
            try:
                r = session.get(url, headers=ozon_headers, params=_params)
            except:
                logger.error(f"{self.featch_data_ozon.__name__}:SessionError")
                return None
            text = r.text
            parser = etree.HTMLParser()
            dom = etree.HTML(text, parser)               
            #cart_class = dom.xpath('//*[@id="layoutPage"]/div[1]/div[3]/div[2]/div[2]/div[5]/div[1]/div/div/div[1]/@class')
            cart_class = 'h6j h7j'
            soup = BeautifulSoup(text, 'lxml')
            books = soup.find('div', class_='widget-search-result-container')
            cart_book = books.find_all('div', class_=cart_class)
            for book in cart_book:
                data_book = {}
                data_book["img"] = book.find('img')['src']
                book_name_author = book.find_all('a', class_='tile-hover-target')[1] \
                .find('span').text.split('|')
                data_book["book"] = book_name_author[0].strip()
                try:
                    data_book["author"] = book_name_author[1].strip()
                except:
                    data_book["author"] = ''
                try:
                    data_book["price"] = "".join(book.find('div', class_="ui-aa3").find('span').text.split()).rstrip('₽')
                except: 
                    data_book["price"] = ''
                data_book["link"] = site+book.find('a')['href']
                data_book["available"] = True
                data_book["source"] = 'Ozon'
                data_book['id'] = str(random.randint(1000,10000))
                self.data.append(data_book)
        
        except:
            logger.error(self.featch_data_ozon.__name__)
            return None
    
    async def featch_data_spbdk(self, session:ClientSession) -> None:
        try:
            site = 'https://www.spbdk.ru'
            link = 'https://www.spbdk.ru/search'
            headers = {'User-Agent':self.user_agent}
            _params = {'q':self.search}
            async with session.get(link, headers=headers, params=_params) as r:
                if r.status != 200:
                    logger.error(f"featch_data_spbdk:{r.status}")
                    return None
                text = await r.text()
                soup = BeautifulSoup(text, 'lxml')
                catalog = soup.find('div', class_='catalog__list').find('div', class_='row')
                books = catalog.find_all('div', class_='col-8')
                for book in books[:6]:
                    data_book = {}
                    data_book["img"] = book.find('a', class_='snippet__photo').find('img')['src']
                    data_book["book"] = book.find('a', class_='snippet__title').text
                    data_book["author"] = book.find('a', class_='snippet__author').text
                    data_book["price"] = book.find('div', class_='snippet__price-value').text.rstrip('q')
                    data_book["link"] = site+book.find('a', class_='snippet__photo')['href']
                    data_book["available"] = True
                    data_book["source"] = 'Spbdk'
                    data_book['id'] = str(random.randint(1000,10000))
                    self.data.append(data_book)
            
        except:
            logger.error(self.featch_data_spbdk.__name__)
            return None

    async def get_book(self) -> List[dict]:
        async with ClientSession() as session:
            get_task = [self.featch_data_bookvoed(session),
                        self.featch_data_book24(session),
                        self.featch_data_fkniga(session),
                        self.featch_data_labirint(session),
                        self.featch_data_ozon(),
                        self.featch_data_spbdk(session)
                        ]

            tasks = list(map(asyncio.create_task, get_task))

            await asyncio.gather(*tasks)
                   
    def main(self):
        asyncio.run(self.get_book())
        return self.data
