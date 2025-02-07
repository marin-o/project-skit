import pytest

from BookstoreApp.models import BookAuthor, BookPublisher, Book


@pytest.mark.parametrize(
    "title, isbn10, isbn13, pages, description, price, cover",
    [
        ("Book1", "1234567890", "1234567890123", 100, "Description1", 10.00, "cover1.jpg"),
        ("Book2", "1234567891", "1234567891123", 200, "Description2", 20.00, "cover2.jpg"),
        ("Book3", "1234567892", "1234567892123", 300, "Description3", 30.00, "cover3.jpg"),
    ]
)
@pytest.mark.django_db
def test_create_valid_book(create_book, title, isbn10, isbn13, pages, description,
                           price, cover):
    """
    Test creating a valid book
    """
    # Arrange
    create_book(title=title, isbn10=isbn10, isbn13=isbn13, pages=pages, description=description, price=price,
                cover=cover)
    # Act
    item = Book.objects.get(title=title)

    # Assert
    assert item.title == title
    assert item.isbn10 == isbn10
    assert item.isbn13 == isbn13
    assert item.pages == pages
    assert item.description == description
    assert item.price == price
    assert item.cover == cover


@pytest.mark.parametrize(
    "title, isbn10, isbn13, pages, description, price, cover",
    [
        ("", "1234567893", "1234567893123", 400, "Description4", 40.00, "cover4.jpg"),
    ]
)
@pytest.mark.django_db
def test_create_invalid_book(create_book, title, isbn10, isbn13, pages, description,
                             price, cover):
    """
    Test creating an invalid book
    """

    # Act and Assert
    with pytest.raises(Exception):
        create_book(title=title, isbn10=isbn10, isbn13=isbn13, pages=pages, description=description,
                    price=price, cover=cover)


@pytest.mark.django_db
def test_book_relationships(create_book):
    """
    Test the relationships between a book, an author, and a publisher
    """

    # Arrange and Act
    book = create_book()

    # Assert
    assert book.bookauthor_set.exists()
    assert book.bookpublisher_set.exists()


@pytest.mark.django_db
def test_invalid_book_relationships(create_author, create_publisher):
    """
    Test associating a book with a non-existent author or publisher
    """

    # Arrange
    book = Book(title="Book1", isbn10="1234567890", isbn13="1234567890123", pages=100, description="Description1",
                price=10.00, cover="cover1.jpg")

    # Act and Assert
    with pytest.raises(Exception):
        BookAuthor.objects.create(book=book, author=create_author.create())

    # Act and Assert
    with pytest.raises(Exception):
        BookPublisher.objects.create(book=book, publisher=create_publisher.create())

