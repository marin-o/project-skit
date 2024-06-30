from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    isbn10 = models.CharField(max_length=10)
    isbn13 = models.CharField(max_length=13)
    pages = models.IntegerField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cover = models.ImageField(upload_to='book_covers/', null=True)

    def __str__(self):
        return self.title


class BookAuthor(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.name + " - " + self.book.title


class Publisher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BookPublisher(models.Model):
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.publisher.name + " - " + self.book.title


@receiver(post_delete, sender=BookAuthor)
def delete_book_if_no_authors(sender, instance, **kwargs):
    if not BookAuthor.objects.filter(book=instance.book).exists():
        instance.book.delete()


@receiver(post_delete, sender=BookPublisher)
def delete_book_if_no_publishers(sender, instance, **kwargs):
    if not BookPublisher.objects.filter(book=instance.book).exists():
        instance.book.delete()