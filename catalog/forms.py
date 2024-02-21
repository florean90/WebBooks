from django import forms
from .models import Book
from datetime import date


class AuthorsForm(forms.Form):
    first_name = forms.CharField(label='The first name of the author')
    last_name = forms.CharField(label='The last name of the author')
    date_of_birth = forms.DateField(label='The date of birth',
                                    initial=format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    date_of_death = forms.DateField(label='The date of death',
                                    initial=format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))


class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'language', 'author', 'summary', 'isbn']


