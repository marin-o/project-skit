from django.shortcuts import render, redirect

from .forms import BookForm
from .models import *
# Create your views here.


def books(request):
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})


def edit_book(request, book_id):
    book = Book.objects.filter(id=book_id).first()
    # edit this book with a forms.ModelForm
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            bookauthors = book.bookauthor_set.all()
            for bookauthor in bookauthors:
                if bookauthor.author not in form.cleaned_data['authors']:
                    bookauthor.delete()

            for author in form.cleaned_data['authors']:
                if not book.bookauthor_set.filter(author=author).exists():
                    BookAuthor.objects.create(book=book, author=author)

            bookpublishers = book.bookpublisher_set.all()
            for bookpublisher in bookpublishers:
                if bookpublisher.publisher not in form.cleaned_data['publishers']:
                    bookpublisher.delete()

            for publisher in form.cleaned_data['publishers']:
                if not book.bookpublisher_set.filter(publisher=publisher).exists():
                    BookPublisher.objects.create(book=book, publisher=publisher)

            book.save()
            return redirect('home')
    else:
        form = BookForm(instance=book)
    return render(request, 'add_or_edit_book.html', {'form': form})


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            for author in form.cleaned_data['authors']:
                BookAuthor.objects.create(book=book, author=author)
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'add_or_edit_book.html', {'form': form})


def delete_book(request, book_id):
    book = Book.objects.filter(id=book_id).first()
    if request.method == 'POST':
        book.delete()
        return redirect('home')
    return render(request, 'delete_book.html', {'book_id': book_id, 'book_title': book.title})
