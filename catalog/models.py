from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter the genre of the book', verbose_name='Book genre')

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=20, help_text='Enter the language of the book', verbose_name='Book language')

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100, help_text='Enter the first name of the author',
                                  verbose_name='Author\'s first name')
    last_name = models.CharField(max_length=100, help_text='Enter the last name of the author',
                                 verbose_name='Author\'s last name')
    date_of_birth = models.DateField(help_text='Enter the date of birth', verbose_name='The date of birth',
                                     null=True, blank=True)
    date_of_death = models.DateField(help_text='Enter the date of death', verbose_name='The date of death',
                                     null=True, blank=True)

    def __str__(self):
        return '{}, {}'.format(self.last_name, self.first_name)


class Book(models.Model):
    title = models.CharField(max_length=200, help_text='Enter the name of the book', verbose_name='Book name')
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, help_text='Choose the genre of the book',
                              verbose_name='Book genre', null=True)
    language = models.ForeignKey('Language', on_delete=models.CASCADE, help_text='Choose the language of the book',
                                 verbose_name='Book language', null=True)
    author = models.ManyToManyField('Author', help_text='Choose the author of the book',
                                    verbose_name='Book author')
    summary = models.TextField(max_length=1000, help_text='Enter a short summary',
                               verbose_name='Book summary')
    isbn = models.CharField(max_length=13, help_text='Must contain 13 symbols', verbose_name='Book ISBN')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_author(self):
        return ', '.join([author.last_name for author in self.author.all()])
    display_author.short_description = 'Authors'


class Status(models.Model):
    name = models.CharField(max_length=20, help_text='Enter the status of the book', verbose_name='Book status')

    def __str__(self):
        return self.name


class BookInstance(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    inv_nom = models.CharField(max_length=20, null=True, help_text='Enter the inventory number of the book instance',
                               verbose_name='Book instance inventory number')
    imprint = models.CharField(max_length=200, help_text='Enter the publisher and the year of release',
                               verbose_name='Book publisher and year of release')
    status = models.ForeignKey('Status', on_delete=models.CASCADE, null=True,
                               help_text='Change the status of the book instance',
                               verbose_name='Book instance status')
    due_back = models.DateField(null=True, blank=True, help_text='Enter the instance due back',
                                verbose_name='Book instance due back')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Borrower',
                                 help_text='Chose the name of the borrower')

    def __str__(self):
        return "%s - %s - %s" % (self.inv_nom, self.book, self.status)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
