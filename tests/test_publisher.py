import pytest
from BookstoreApp.models import Publisher


@pytest.mark.django_db
def test_create_publisher(publisher_factory):
    publisher = publisher_factory(name='Publisher1')

    assert Publisher.objects.filter(name='Publisher1').exists()


@pytest.mark.django_db
def test_publisher_name_validation(publisher_factory):
    with pytest.raises(Exception):
        publisher_factory(name='')
