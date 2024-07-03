import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize('setup_delete_data', ['book', 'author', 'publisher'], indirect=True)
def test_delete_instance(client, setup_delete_data):
    """
    Test delete views
    """

    # Arrange
    instance, url_name, redirect_url = setup_delete_data

    # Act
    url = reverse(url_name, args=[instance.pk])

    # Assert
    response = client.get(url)
    assert response.status_code == 200
    if hasattr(instance, "name"):
        assert instance.name.encode() in response.content
    else:
        assert instance.title.encode() in response.content

    response = client.post(url)
    assert response.status_code == 302
    assert redirect_url in response.url
    model = instance.__class__
    assert not model.objects.filter(pk=instance.pk).exists()
