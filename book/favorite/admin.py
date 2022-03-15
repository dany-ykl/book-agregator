from django.contrib import admin
from . import models


admin.site.register(models.Customer)
admin.site.register(models.BasketItem)
admin.site.register(models.Basket)
