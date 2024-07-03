import pytest
from BookstoreApp.models import Publisher


@pytest.mark.django_db
def test_create_publisher(create_publisher):
    publisher = create_publisher(name='Publisher1')

    assert Publisher.objects.filter(name='Publisher1').exists()


@pytest.mark.django_db
def test_publisher_name_validation(create_publisher):
    with pytest.raises(Exception):
        create_publisher(name='')
