import pytest
from BookstoreApp.forms import BookForm, AuthorForm, PublisherForm
from BookstoreApp.models import Book, Author, Publisher


@pytest.mark.django_db
def test_valid_book_form(create_book, create_author, create_publisher):
    create_author()
    create_publisher()
    book = create_book(cover='')
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
def test_valid_author_form(create_author):
    author = create_author()
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
def test_valid_publisher_form(create_publisher):
    publisher = create_publisher()
    data = {
        'name': publisher.name,
    }
    form = PublisherForm(data=data)
    assert form.is_valid()


@pytest.mark.django_db
def test_invalid_publisher_form():
    form = PublisherForm(data={})
    assert not form.is_valid()