from django.forms import ModelForm
from django.forms import ModelMultipleChoiceField

from BookstoreApp.models import Book, Author, Publisher


class BookForm(ModelForm):
    authors = ModelMultipleChoiceField(queryset=Author.objects.all())
    publishers = ModelMultipleChoiceField(queryset=Publisher.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['cover'].required = False
        if self.instance.pk:  # if this is an existing book
            self.fields['authors'].initial = self.instance.bookauthor_set.values_list('author', flat=True)
            self.fields['publishers'].initial = self.instance.bookpublisher_set.values_list('publisher', flat=True)

    class Meta:
        model = Book
        fields = '__all__'


class AuthorForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Author
        fields = '__all__'


class PublisherForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Publisher
        fields = '__all__'
