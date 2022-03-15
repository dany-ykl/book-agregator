from typing import List
from fake_useragent import UserAgent


def user_agent():
    try:
        return UserAgent().random
    except IndexError:
        return None


def unpacking(list_book:List[dict]) -> List[dict]:
    books = []
    for source in range(0, len(list_book)):
        for book in list_book[source]:
            books.append(book)
    return books