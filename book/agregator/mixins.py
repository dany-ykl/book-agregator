from django.views.generic import View
from favorite.models import Customer, Basket


class CustomerMixin(View):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(user=request.user)
                basket = Basket.objects.create(owner=customer)

            basket = Basket.objects.filter(owner=customer).first()

        else:
            customer = Customer.objects.filter(session_id=request.session.session_key).first()
            if not customer:
                customer = Customer.objects.create(session_id=request.session.session_key, anonymos_user=True)
            
            basket = Basket.objects.filter(owner=customer).first()
            if not basket:
                basket = Basket.objects.create(owner=customer)

        self.customer = customer
        self.basket = basket

        return super().dispatch(request, *args, **kwargs)