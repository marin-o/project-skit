import pytest

from pytest_factoryboy import register
from tests.factories import *

register(AuthorFactory)
register(PublisherFactory)
register(BookFactory)

