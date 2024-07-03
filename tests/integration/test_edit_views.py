import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize("fixture, url_name, field_to_check, new_value", [
    ('setup_book_edit_data', 'edit_book', 'title', 'New Title'),
    ('setup_author_edit_data', 'edit_author', 'name', 'New Name'),
    ('setup_publisher_edit_data', 'edit_publisher', 'name', 'New Name'),
])
def test_edit_views(client, request, fixture, url_name, field_to_check, new_value):
    instance, data = request.getfixturevalue(fixture)
    url = reverse(url_name, args=[instance.pk])
    response = client.get(url)
    assert response.status_code == 200

    if field_to_check in data:
        data[field_to_check] = new_value

    response = client.post(url, data)
    assert response.status_code == 302

    instance.refresh_from_db()
    assert getattr(instance, field_to_check) == new_value
