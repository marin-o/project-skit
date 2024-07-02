import pytest
from BookstoreApp.models import Author


@pytest.mark.django_db
def test_create_author(create_author):
    author = create_author(name="Author1")

    assert Author.objects.filter(name="Author1").exists()


@pytest.mark.django_db
def test_author_name_validation(create_author):
    with pytest.raises(Exception):
        create_author(name='')
