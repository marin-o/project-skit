# Generated by Django 5.0.6 on 2024-06-10 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookstoreApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.ImageField(null=True, upload_to='book_covers/'),
        ),
    ]
