import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize("url_name, create_batch, expected_count", [
    ("home", "create_book_batch", 5),
    ("authors", "create_author_batch", 5),
    ("publishers", "create_publisher_batch", 5),
])
def test_views(client, request, url_name, create_batch, expected_count):
    create_batch = request.getfixturevalue(create_batch)
    items = create_batch(expected_count)

    url = reverse(url_name)
    response = client.get(url)

    assert response.status_code == 200

    for item in items:
        if hasattr(item, "name"):
            assert item.name.encode() in response.content
        else:
            item.title.encode() in response.content
