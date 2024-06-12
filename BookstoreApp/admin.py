from django.contrib import admin

from BookstoreApp.models import *

# Register your models here.


class BookAuthorInline(admin.StackedInline):
    model = BookAuthor
    extra = 1


class BookPublisherInline(admin.StackedInline):
    model = BookPublisher
    extra = 1


class BookAdmin(admin.ModelAdmin):
    inlines = [BookAuthorInline, BookPublisherInline]


admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(BookAuthor)
admin.site.register(BookPublisher)
