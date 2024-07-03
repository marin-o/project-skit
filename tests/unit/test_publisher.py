import pytest
from BookstoreApp.models import Publisher


@pytest.mark.django_db
def test_create_publisher(create_publisher):
    """
    Test creating a valid publisher
    """
    # Arrange and Act
    publisher = create_publisher(name='Publisher1')

    # Assert
    assert Publisher.objects.filter(name='Publisher1').exists()


@pytest.mark.django_db
def test_publisher_name_validation(create_publisher):
    """
    Test creating a publisher with an empty name
    """

    # Act and Assert
    with pytest.raises(Exception):
        create_publisher(name='')
