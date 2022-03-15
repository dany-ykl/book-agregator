from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView

from .forms import CustomUserCreationForm
from .accounts_service import _validate_email


def validate_email(request):
    return _validate_email(request)

class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('agregator:home-view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notsearch'] = True
        return context

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            return super(RegisterView, self).form_valid(form)

    def get(self,  *args, **kwargs):
        return super(RegisterView, self).get(*args, **kwargs)


class LoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notsearch'] = True
        return context

    def get_success_url(self):
        return reverse_lazy('agregator:home-view')


class LogoutView(LogoutView):
    next_page = 'agregator:home-view'