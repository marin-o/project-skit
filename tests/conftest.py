import pytest
from django.urls import reverse
from selenium import webdriver

from BookstoreApp.models import Author, Publisher
from tests.factories import AuthorFactory, PublisherFactory, BookFactory


@pytest.fixture
def create_author():
    """
    Creates an instance of Author using the AuthorFactory.
    """
    def _author_factory(**kwargs):
        return AuthorFactory.create(**kwargs)
    return _author_factory


@pytest.fixture
def create_publisher():
    """
    Creates an instance of Publisher using the PublisherFactory.
    """
    def _publisher_factory(**kwargs):
        return PublisherFactory.create(**kwargs)
    return _publisher_factory


@pytest.fixture
def create_book():
    """
    Creates an instance of Book using the BookFactory.
    """
    def _book_factory(**kwargs):
        return BookFactory.create(**kwargs)
    return _book_factory


@pytest.fixture
def create_author_batch():
    """
    Creates a batch of Author instances using the AuthorFactory.
    """
    def _author_batch(batch_size=5, **kwargs):
        return AuthorFactory.create_batch(batch_size, **kwargs)
    return _author_batch


@pytest.fixture
def create_publisher_batch():
    """
    Creates a batch of Publisher instances using the PublisherFactory.
    """
    def _publisher_batch(batch_size=5, **kwargs):
        return PublisherFactory.create_batch(batch_size, **kwargs)
    return _publisher_batch


@pytest.fixture
def create_book_batch():
    """
    Creates a batch of Book instances using the BookFactory.
    """
    def _book_batch(batch_size=5, **kwargs):
        return BookFactory.create_batch(batch_size, **kwargs)
    return _book_batch


@pytest.fixture
def setup_delete_data(request, create_book, create_author, create_publisher):
    """
    Sets up data for testing deletion of Book, Author, or Publisher.

    Parameters:
    - request: pytest request object.
    - create_book: Fixture to create a Book instance.
    - create_author: Fixture to create an Author instance.
    - create_publisher: Fixture to create a Publisher instance.

    Returns:
    - tuple: Instance of the model to delete, URL name for deletion view, and redirection URL after deletion.
    """
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
    """
    Sets up data for testing editing a Book.

    Parameters:
    - create_book: Fixture to create a Book instance.

    Returns:
    - tuple: Instance of the Book to edit and data dictionary for editing.
    """
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
    """
    Sets up data for testing editing an Author.

    Parameters:
    - create_author: Fixture to create an Author instance.

    Returns:
    - tuple: Instance of the Author to edit and data dictionary for editing.
    """
    author = create_author()
    data = {'name': 'New Name'}
    return author, data


@pytest.fixture
def setup_publisher_edit_data(create_publisher):
    """
    Sets up data for testing editing a Publisher.

    Parameters:
    - create_publisher: Fixture to create a Publisher instance.

    Returns:
    - tuple: Instance of the Publisher to edit and data dictionary for editing.
    """
    publisher = create_publisher()
    data = {'name': 'New Name'}
    return publisher, data


@pytest.fixture(scope='class', params=['chrome'])
def driver_init(request):
    """
    Initializes a WebDriver instance for browser testing.

    Parameters:
    - request: pytest request object.

    Yields:
    - WebDriver: Initialized WebDriver instance.

    After the test(s) using this fixture, quits the WebDriver.
    """
    if request.param == 'chrome':
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
    # elif request.param == 'firefox':
    #     options = webdriver.FirefoxOptions()
    #     options.add_argument('--headless')
    #     driver = webdriver.Firefox(options=options)
    request.cls.driver = driver
    yield
    driver.quit()
