import pytest
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
