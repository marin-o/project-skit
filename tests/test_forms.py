import pytest
from BookstoreApp.forms import BookForm, AuthorForm, PublisherForm
from BookstoreApp.models import Book, Author, Publisher


@pytest.mark.django_db
def test_valid_book_form(book_factory, author_factory, publisher_factory):
    author_factory()
    publisher_factory()
    book = book_factory(cover='')
    data = {
        'title': book.title,
        'isbn10': book.isbn10,
        'isbn13': book.isbn13,
        'pages': book.pages,
        'description': book.description,
        'price': book.price,
        'cover': '',
        'authors': [author.pk for author in Author.objects.all()],
        'publishers': [publisher.pk for publisher in Publisher.objects.all()],
    }
    form = BookForm(data=data)
    assert form.is_valid()


@pytest.mark.django_db
def test_invalid_book_form():
    form = BookForm(data={})
    assert not form.is_valid()


@pytest.mark.django_db
def test_valid_author_form(author_factory):
    author = author_factory()
    data = {
        'name': author.name,
    }
    form = AuthorForm(data=data)
    assert form.is_valid()


@pytest.mark.django_db
def test_invalid_author_form():
    form = AuthorForm(data={})
    assert not form.is_valid()


@pytest.mark.django_db
def test_valid_publisher_form(publisher_factory):
    publisher = publisher_factory()
    data = {
        'name': publisher.name,
    }
    form = PublisherForm(data=data)
    assert form.is_valid()


@pytest.mark.django_db
def test_invalid_publisher_form():
    form = PublisherForm(data={})
    assert not form.is_valid()