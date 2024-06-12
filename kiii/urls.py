"""
URL configuration for kiii project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from kiii import settings
from BookstoreApp.views import books, edit_book, add_book, delete_book

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', books, name='home'),
    path('index/', books, name='home'),
    path('books/', books, name='home'),
    path('edit_book/<int:book_id>', edit_book, name='edit_book'),
    path('add_book/', add_book, name='add_book'),
    path('delete_book/<int:book_id>', delete_book, name='delete_book'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
