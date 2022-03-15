class ResourceNotFoundBook(Exception):
    pass

class SearchError(Exception):
    pass

class RequestError(Exception):
    
    def __str__(self) -> str:
        return "Request error"
