from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
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
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('home')
    return render(request, 'delete_book.html', {'book_id': book_id, 'book_title': book.title})


def authors(request):
    authors = Author.objects.all()
    return render(request, 'authors.html', {'authors': authors})


def publishers(request):
    publishers = Publisher.objects.all()
    return render(request, 'publishers.html', {'publishers': publishers})


def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('authors')
    else:
        form = AuthorForm()
    return render(request, 'add_or_edit_author.html', {'form': form})


def add_publisher(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('publishers')
    else:
        form = PublisherForm()
    return render(request, 'add_or_edit_publisher.html', {'form': form})


def edit_author(request, author_id):
    author = Author.objects.filter(id=author_id).first()
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('authors')
    else:
        form = AuthorForm(instance=author)
    return render(request, 'add_or_edit_author.html', {'form': form})


def delete_author(request, author_id):
    author = Author.objects.filter(id=author_id).first()
    if request.method == 'POST':
        author.delete()
        return redirect('authors')
    return render(request, 'delete_author.html', {'author_id': author_id, 'author_name': author.name})


def edit_publisher(request, publisher_id):
    publisher = Publisher.objects.filter(id=publisher_id).first()
    if request.method == 'POST':
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            form.save()
            return redirect('publishers')
    else:
        form = PublisherForm(instance=publisher)
    return render(request, 'add_or_edit_publisher.html', {'form': form})


def delete_publisher(request, publisher_id):
    publisher = Publisher.objects.filter(id=publisher_id).first()
    if request.method == 'POST':
        publisher.delete()
        return redirect('publishers')
    return render(request, 'delete_publisher.html', {'publisher_id': publisher_id, 'publisher_name': publisher.name})
