import pytest
from BookstoreApp.models import Author


@pytest.mark.django_db
def test_create_author(author_factory):
    author = author_factory(name="Author1")

    assert Author.objects.filter(name="Author1").exists()


@pytest.mark.django_db
def test_author_name_validation(author_factory):
    with pytest.raises(Exception):
        author_factory(name='')
