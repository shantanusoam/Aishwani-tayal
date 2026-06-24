from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("ccts/", views.services, name="ccts"),
    path("about/", views.about, name="about"),
    path("blogs/", views.blogs, name="blogs"),
    path("book-consultation/", views.book_consultation, name="book_consultation"),
]
