import pytest
from django.urls import reverse
from BookstoreApp.models import Book, Author, Publisher


@pytest.mark.django_db
def test_books_view(client, create_book_batch):
    books = create_book_batch(5)

    url = reverse("home")
    response = client.get(url)

    assert response.status_code == 200

    for book in books:
        assert book.title.encode() in response.content


@pytest.mark.django_db
def test_authors_view(client, create_author_batch):
    authors = create_author_batch(5)

    url = reverse("authors")
    response = client.get(url)

    assert response.status_code == 200

    for author in authors:
        assert author.name.encode() in response.content


@pytest.mark.django_db
def test_publishers_view(client, create_publisher_batch):
    publishers = create_publisher_batch(5)

    url = reverse("publishers")
    response = client.get(url)

    assert response.status_code == 200

    for publisher in publishers:
        assert publisher.name.encode() in response.content
