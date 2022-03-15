from logging import PlaceHolder
from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder':'Введите название книги'}))
    