from django.urls import path
from main.models import setting
from main.Backend.cleanDatabase import checkDatabase
from main.Backend.update import autoUpdate, updateOnStart
import threading
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

## urls.py is top level, so startup code can be written here to be executed once
checkDatabase()

if setting.objects.get(name="automaticUpdates").state == True:
    t = threading.Thread(target=autoUpdate, args=(setting.objects.get(name="automaticUpdates").value, ))
    t.setDaemon = True
    t.start()

else:
    t = threading.Thread(target=updateOnStart)
    t.setDaemon = True
    t.start()