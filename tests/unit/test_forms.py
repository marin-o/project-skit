import pytest

from BookstoreApp.forms import BookForm, AuthorForm, PublisherForm
from BookstoreApp.models import Author, Publisher


@pytest.mark.django_db
def test_valid_book_form(create_book, create_author, create_publisher):
    """
    Test creating a valid book through the form
    """

    # Arrange
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

    # Act
    form = BookForm(data=data)

    # Assert
    assert form.is_valid()


@pytest.mark.django_db
def test_invalid_book_form():
    """
    Test creating an invalid book through the form
    """

    # Arrange and Act
    form = BookForm(data={})

    # Assert
    assert not form.is_valid()


@pytest.mark.django_db
def test_valid_author_form(create_author):
    """
    Test creating a valid author through the form
    """

    # Arrange
    author = create_author()
    data = {
        'name': author.name,
    }

    # Act
    form = AuthorForm(data=data)

    # Assert
    assert form.is_valid()


@pytest.mark.django_db
def test_invalid_author_form():
    """
    Test creating an invalid author through the form
    """

    # Arrange and Act
    form = AuthorForm(data={})

    # Assert
    assert not form.is_valid()


@pytest.mark.django_db
def test_valid_publisher_form(create_publisher):
    """
    Test creating a valid publisher through the form
    """

    # Arrange
    publisher = create_publisher()
    data = {
        'name': publisher.name,
    }

    # Act
    form = PublisherForm(data=data)

    # Assert
    assert form.is_valid()


@pytest.mark.django_db
def test_invalid_publisher_form():
    """
    Test creating an invalid publisher through the form
    """

    # Arrange and Act
    form = PublisherForm(data={})

    # Assert
    assert not form.is_valid()
