from django.urls import path
from django.views import static
from . import views

urlpatterns = [
    path("", views.redirect_view, name="redirect"),
    path("library/", views.library, name="library"),
    path("browse/", views.browse, name="browse"),
    path("novel/<int:id>", views.novel, name="novel"),
    path("comic/<int:id>", views.comic, name="comic")
]
