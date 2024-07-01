import factory
from faker import Faker
from django.contrib.auth.models import User
from BookstoreApp.models import *

fake = Faker()


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    name = fake.name()


class PublisherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Publisher

    name = ' '.join(fake.words(nb=2))


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = ' '.join(fake.words(nb=2))
    isbn10 = fake.isbn10()
    isbn13 = fake.isbn13()
    pages = fake.random_int()
    description = fake.text(100)
    price = fake.random_int()
    cover = fake.image_url()

    @factory.post_generation
    def authors_and_publishers(self, create, extracted, **kwargs):
        if not create:
            return

        author = AuthorFactory.create()
        publisher = PublisherFactory.create()

        BookAuthor.objects.create(book=self, author=author)
        BookPublisher.objects.create(book=self, publisher=publisher)

        author.save()
        publisher.save()
        self.save()
