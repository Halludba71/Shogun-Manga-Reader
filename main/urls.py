from django.urls import path
from django.views import static
from . import views

urlpatterns = [
    path("", views.redirect_view, name="redirect"),
    path("library/", views.library, name="library"),
    path("browse/", views.browse, name="browse"),
    path("extensions/", views.extensions, name="extensions"),
    path("novel/<int:id>", views.novel, name="novel"),
    path("comic/<int:inLibrary>/<int:id>", views.comic, name="comic"),
    path("read/<int:inLibrary>/<int:comicId>/<int:chapterId>", views.read, name="read"),
    path("bypass/<path:imageUrl>", views.bypass, name="bypass")
]
