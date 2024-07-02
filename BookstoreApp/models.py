from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.name:
            raise Exception("Name is required")
        super(Author, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    isbn10 = models.CharField(max_length=13)
    isbn13 = models.CharField(max_length=17)
    pages = models.IntegerField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cover = models.ImageField(upload_to='book_covers/', null=True)

    def save(self, *args, **kwargs):
        required_fields = ['title', 'isbn10', 'isbn13', 'pages', 'description', 'price']

        for field_name in required_fields:
            value = getattr(self, field_name)
            if not value:
                raise Exception(f"{field_name.capitalize()} is required")

        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class BookAuthor(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.author:
            raise Exception("Author is required")
        if not self.book:
            raise Exception("Book is required")
        super(BookAuthor, self).save(*args, **kwargs)

    def __str__(self):
        return self.author.name + " - " + self.book.title


class Publisher(models.Model):
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.name:
            raise Exception("Name is required")
        super(Publisher, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class BookPublisher(models.Model):
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.publisher:
            raise Exception("Publisher is required")
        if not self.book:
            raise Exception("Book is required")
        super(BookPublisher, self).save(*args, **kwargs)

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