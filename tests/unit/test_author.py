import pytest
from BookstoreApp.models import Author


@pytest.mark.django_db
def test_create_author(create_author):
    """
    Test that an author can be created
    """

    # Arrange
    author = create_author(name="Author1")

    # Act and Assert
    assert Author.objects.filter(name="Author1").exists()


@pytest.mark.django_db
def test_author_name_validation(create_author):
    """
    Test that an exception is raised when an empty string is passed as the name
    """

    # Act and Assert
    with pytest.raises(Exception):
        create_author(name='')
