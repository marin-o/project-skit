import pytest
from django.urls import reverse
from selenium import webdriver

from BookstoreApp.models import Author, Publisher, Book
from tests.factories import AuthorFactory, PublisherFactory, BookFactory


@pytest.fixture
def create_author():
    def _author_factory(**kwargs):
        return AuthorFactory.create(**kwargs)
    return _author_factory


@pytest.fixture
def create_publisher():
    def _publisher_factory(**kwargs):
        return PublisherFactory.create(**kwargs)
    return _publisher_factory


@pytest.fixture
def create_book():
    def _book_factory(**kwargs):
        return BookFactory.create(**kwargs)
    return _book_factory


@pytest.fixture
def create_author_batch():
    def _author_batch(batch_size=5, **kwargs):
        return AuthorFactory.create_batch(batch_size, **kwargs)
    return _author_batch


@pytest.fixture
def create_publisher_batch():
    def _publisher_batch(batch_size=5, **kwargs):
        return PublisherFactory.create_batch(batch_size, **kwargs)
    return _publisher_batch


@pytest.fixture
def create_book_batch():
    def _book_batch(batch_size=5, **kwargs):
        return BookFactory.create_batch(batch_size, **kwargs)
    return _book_batch


@pytest.fixture
def setup_delete_data(request, create_book, create_author, create_publisher):
    model_type = request.param
    if model_type == 'book':
        instance = create_book()
        url_name = "delete_book"
        redirect_url = reverse("home")
    elif model_type == 'author':
        instance = create_author()
        url_name = "delete_author"
        redirect_url = reverse("authors")
    elif model_type == 'publisher':
        instance = create_publisher()
        url_name = "delete_publisher"
        redirect_url = reverse("publishers")
    else:
        raise ValueError("Invalid model type")
    return instance, url_name, redirect_url


@pytest.fixture
def setup_book_edit_data(create_book):
    book = create_book()
    data = {
        'title': 'New Title',
        'isbn10': book.isbn10,
        'isbn13': book.isbn13,
        'pages': book.pages,
        'description': book.description,
        'price': book.price,
        'cover': '',
        'authors': [author.pk for author in Author.objects.all()],
        'publishers': [publisher.pk for publisher in Publisher.objects.all()],
    }
    return book, data


@pytest.fixture
def setup_author_edit_data(create_author):
    author = create_author()
    data = {'name': 'New Name'}
    return author, data


@pytest.fixture
def setup_publisher_edit_data(create_publisher):
    publisher = create_publisher()
    data = {'name': 'New Name'}
    return publisher, data


@pytest.fixture(scope='class', params=['chrome', 'firefox'])
def driver_init(request):
    if request.param == 'chrome':
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
    elif request.param == 'firefox':
        options = webdriver.FirefoxOptions()
        # options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
    request.cls.driver = driver
    yield
    driver.close()


@pytest.fixture(scope='class')
def create_book_batch_class():
    def _book_batch(batch_size=5, **kwargs):
        return BookFactory.create_batch(batch_size, **kwargs)
    return _book_batch


@pytest.fixture(scope='class')
def create_book_batch_e2e():
    books = BookFactory.create_batch(5)
    for book in books:
        book.title = f"Book {book.pk}"
        book.save()
    yield
    for book in books:
        if Book.objects.filter(pk=book.pk).exists():
            book.delete()
