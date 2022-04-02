from django.urls import path
from django.views import static
from . import views

urlpatterns = [
    path("", views.redirect_view, name="redirect"),
    path("library/", views.library, name="library"),
    path("browse/", views.browse, name="browse"),
    path("extensions/", views.extensions, name="extensions"),
    path("extensions/linkedManga/", views.linkedManga, name="linkedManga"),
    path("comic/<int:inLibrary>/<int:id>", views.comic, name="comic"),
    path("read/<int:inLibrary>/<int:comicId>/<int:chapterIndex>", views.read, name="read"), 
    path("bypass/<int:extensionId>/<path:imageUrl>", views.bypass, name="bypass"),
    path("downloads/", views.downloads, name="downloads"),
    path("downloads/progress/", views.downloadProgress, name="downloadProgress"),
    path("settings/", views.settings, name="settings")
]
