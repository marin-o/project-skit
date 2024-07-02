import pytest
from tests.factories import AuthorFactory, PublisherFactory, BookFactory


@pytest.fixture
def author_factory():
    def _author_factory(**kwargs):
        return AuthorFactory.create(**kwargs)
    return _author_factory


@pytest.fixture
def publisher_factory():
    def _publisher_factory(**kwargs):
        return PublisherFactory.create(**kwargs)
    return _publisher_factory


@pytest.fixture
def book_factory():
    def _book_factory(**kwargs):
        return BookFactory.create(**kwargs)
    return _book_factory


