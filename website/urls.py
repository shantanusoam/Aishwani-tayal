from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("book-consultation/", views.book_consultation, name="book_consultation"),
]
